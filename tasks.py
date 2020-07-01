from pprint import pprint
from time import sleep
from uuid import uuid4

from boto3.session import Config, Session
from invoke import task

ACM_REGION = 'us-east-1'
ACM_WAIT_TIME = 15
CALLER_REFERENCE = str(uuid4())


def aws_client(c, service, region):
    config = c.config.bigga
    session = Session(region_name=region)
    return session.client(
        service, config=Config(signature_version='s3v4'),
        aws_access_key_id=config.key_id,
        aws_secret_access_key=config.secret_key)


def get_bucket_name(environment, product_name):
    return f'app{environment}-{product_name}'


def get_bucket_origin(environment, product_name):
    bucket_name = get_bucket_name(environment, product_name)
    return f'{bucket_name}.s3.amazonaws.com'


def get_bucket_origin_id(environment, product_name):
    bucket_name = get_bucket_name(environment, product_name)
    return f'S3-{bucket_name}'


@task
def zombies(c, kill=False):
    '''list (or kill [-k]) zombie processes'''
    ps = []
    ls = c.run('docker ps').stdout.split('\n')[1:-1]
    for line in ls:
        container, image = line.split()[:2]
        if 'bigga' not in image and ':' not in image:
            ps.append(container)

    print("Zombies: ", " ".join(ps))
    if kill:
        c.run(f'docker kill {" ".join(ps)}')


@task(help={
    'service': "Which service's region do you want to list? default: s3",
})
def list_regions(s, service='s3'):
    s = Session()
    regions = s.get_available_regions(service)
    pprint(regions)


@task(help={
    'domains': 'Primary domain followed by list of all other domains',
    'region': "run `inv list-regions to get a list of regions`",
    'environment': 'beta | qa | prod | stag',
}, iterable=['domains'])
def init_s3_cf_app(c, region, environment, domains):
    '''
    Init S3 CloudFront App
    '''

    # Create Bucket
    s3 = aws_client(c, 's3', region)
    bucket_name = get_bucket_name(environment, c.config.bigga.product_name)
    response = s3.create_bucket(
        ACL='public-read',
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': region
        },
        # GrantFullControl='string',
        # GrantRead='string',
        # GrantReadACP='string',
        # GrantWrite='string',
        # GrantWriteACP='string',
        # ObjectLockEnabledForBucket=True|False
    )
    pprint(response)
    print('Bucket Created')
    print('Bucket: ', bucket_name)
    '''
    print('Configuring bucket to host website...')
    response = s3.put_bucket_website(
        Bucket=bucket_name,
        WebsiteConfiguration={
            'ErrorDocument': {
                'Key': 'index.html'
            },
            'IndexDocument': {
                'Suffix': 'index.html'
            },
        }
    )
    pprint(response)
    pprint('Bucket Configured to host website')
    print('Bucket: ', bucket_name)
    '''

    # Generate ACM Certs
    acm = aws_client(c, 'acm', ACM_REGION)
    d = dict(
        DomainName=domains[0],
        ValidationMethod='DNS',
        # IdempotencyToken='string',
        Options={
            'CertificateTransparencyLoggingPreference': 'ENABLED'
        },
    )
    if domains[1:]:
        d['SubjectAlternativeNames'] = domains[1:],
    response = acm.request_certificate(**d)
    cert_arn = response['CertificateArn']
    print(f'Waiting {ACM_WAIT_TIME} seconds to generate DNS Records')
    sleep(ACM_WAIT_TIME)
    print('Certificate Details:')
    response = acm.describe_certificate(CertificateArn=cert_arn)
    cert_data = response['Certificate']
    opt = 'DomainValidationOptions'
    dns_data = cert_data[opt]
    print('DNS Verificxation Details:')
    pprint(dns_data)
    print('Certificate ARN: ', cert_arn)
    while True:
        response = acm.describe_certificate(CertificateArn=cert_arn)
        cert_data = response['Certificate']
        print('Waiting for validation')
        print(cert_data['Status'])
        if cert_data['Status'] == 'ISSUED':
            break
        sleep(ACM_WAIT_TIME)

    # Create CF Distribution
    cf = aws_client(c, 'cloudfront', region)
    bucket_name = get_bucket_name(environment, c.config.bigga.product_name)
    origin_domain = get_bucket_origin(environment, c.config.bigga.product_name)
    origin_id = get_bucket_origin_id(environment, c.config.bigga.product_name)
    print(origin_id, origin_domain)
    response = cf.create_distribution(
        DistributionConfig={
            'CallerReference': CALLER_REFERENCE,
            'Aliases': {
                'Quantity': len(domains),
                'Items': domains
            },
            'DefaultRootObject': 'index.html',
            'Origins': {
                'Quantity': 1,
                'Items': [
                    {
                        'Id': origin_id,
                        'DomainName': origin_domain,
                        # 'OriginPath': 'string',
                        'S3OriginConfig': {
                            'OriginAccessIdentity': ''
                        },
                    },
                ]
            },
            'DefaultCacheBehavior': {
                'TargetOriginId': origin_id,
                'ForwardedValues': {
                    'QueryString': False,
                    'Cookies': {
                        'Forward': 'none',
                    },
                },
                'TrustedSigners': {
                    'Enabled': False,
                    'Quantity': 0,
                    'Items': [
                    ]
                },
                'ViewerProtocolPolicy': 'redirect-to-https',
                'MinTTL': 0,
                'AllowedMethods': {
                    'Quantity': 2,
                    'Items': ['GET', 'HEAD'],
                    'CachedMethods': {
                        'Quantity': 2,
                        'Items': ['GET', 'HEAD']
                    }
                },
                'SmoothStreaming': False,
                'Compress': True,
            },
            'CustomErrorResponses': {
                'Quantity': 1,
                'Items': [
                    {
                        'ErrorCode': 404,
                        'ResponsePagePath': '/index.html',
                        'ResponseCode': '200',
                        # 'ErrorCachingMinTTL': 123
                    },
                ]
            },
            'Comment': f'CF Dist for {bucket_name}',
            'Logging': {
                'Enabled': False,
                'IncludeCookies': False,
                'Bucket': '',
                'Prefix': ''
            },
            'PriceClass': 'PriceClass_All',
            'ViewerCertificate': {
                'CloudFrontDefaultCertificate': False,
                'ACMCertificateArn': cert_arn,
                'SSLSupportMethod': 'sni-only',
                'MinimumProtocolVersion': 'TLSv1.2_2018',
            },
            'Enabled': True,
        }
    )
    print(response)
