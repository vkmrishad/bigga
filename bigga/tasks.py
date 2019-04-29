import json
import logging
import requests
from invoke import task
from posixpath import join
from fabric import Connection
from urllib.parse import quote

from patchwork import files as pw_files
from bigga.contrib.fabtools.user import home_directory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
BIGGA_DATA = json.load(open('.bigga.json'))
SSH_USERS = ['dhilipsiva']


@task
def echo(c, env):  # , app, env):
    for host in BIGGA_DATA['hosts'][env]:
        cxn = Connection(host['ip'], user=host['user'])
        cxn.run('echo foo')


@task
def sync_auth_keys(c, env):
    # Add multiple public keys to the user's authorized SSH keys from GitHub.
    for host in BIGGA_DATA['hosts'][env]:
        cxn = Connection(host['ip'], user=host['user'])
        ssh_dir = join(home_directory(cxn), '.ssh')
        pw_files.directory(cxn, ssh_dir, mode='700')
        authorized_keys_filename = join(ssh_dir, 'authorized_keys')
        cxn.run('cat /dev/null > %s' % quote(authorized_keys_filename))
        logger.info('Fetching public keys from GitHub')
        for gh_user in SSH_USERS:
            r = requests.get('https://api.github.com/users/%s/keys' % gh_user)
            for key in r.json():
                cxn.run('echo %s >> %s' % (
                    quote(key['key']), quote(authorized_keys_filename)))
