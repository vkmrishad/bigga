from time import sleep
from pprint import pprint

from boto3.session import Config, Session
from invoke import task

ACM_REGION = 'us-east-1'
ACM_WAIT_TIME = 15


def aws_client(c, service, region):
    config = c.config.bigga
    session = Session(region_name=region)
    return session.client(
        service, config=Config(signature_version='s3v4'),
        aws_access_key_id=config.key_id,
        aws_secret_access_key=config.secret_key)


def get_bucket_name(environment, product_name):
    return f'app{environment}-{product_name}'


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


@task
def list_regions(s, service='s3'):
    s = Session()
    regions = s.get_available_regions(service)
    pprint(regions)


@task(help={
    'region': "run `inv list-regions to get a list of regions`",
    'environment': 'beta | qa | prod | stag',
})
def create_bucket(c, region, environment):
    client = aws_client(c, 's3', region)
    bucket_name = get_bucket_name(environment, c.config.bigga.product_name)
    response = client.create_bucket(
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
    print('Configuring bucket to host website...')
    response = client.put_bucket_website(
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


@task(help={
    'domain': 'Domain to generate certificate for',
})
def request_certificate(c, domain):
    client = aws_client(c, 'acm', ACM_REGION)
    response = client.request_certificate(
        DomainName=domain,
        ValidationMethod='DNS',
        # SubjectAlternativeNames=['more.example.com'],
        # IdempotencyToken='string',
        Options={
            'CertificateTransparencyLoggingPreference': 'ENABLED'
        },
    )
    print('Certificate requested')
    cert_arn = response['CertificateArn']
    print(f'Waiting {ACM_WAIT_TIME} seconds to generate DNS Records')
    sleep(ACM_WAIT_TIME)
    print('Certificate Details:')
    response = client.describe_certificate(CertificateArn=cert_arn)
    cert_data = response['Certificate']
    opt = 'DomainValidationOptions'
    dns_data = cert_data[opt]
    print('DNS Verificxation Details:')
    pprint(dns_data)
    print('Certificate ARN: ', cert_arn)
