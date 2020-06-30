from pprint import pprint

from boto3.session import Config, Session
from invoke import task


def aws_client(service, region, config):
    session = Session(region_name=region)
    return session.client(
        service, config=Config(signature_version='s3v4'),
        aws_access_key_id=config.key_id,
        aws_secret_access_key=config.secret_key)


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
    config = c.config.bigga
    client = aws_client('s3', region, config)
    bucket_name = f'app{environment}'
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
    __import__('ipdb').set_trace()
