from typing import Set, Dict
from dataclasses import dataclass
from json import dumps as jdumps, load as jload

from fabric import Connection

BIGGA_JSON = '.bigga.json'


class DataClassMixin(object):

    def dumps(self, **kwargs) -> str:
        return jdumps(self, default=lambda o: o.__dict__, **kwargs)

    @staticmethod
    def load(data: Dict):
        raise NotImplementedError('Please implement load()')


@dataclass
class Service(DataClassMixin):
    name: str
    framework: str
    args: Dict[str, str]

    @staticmethod
    def load(data: Dict):
        return Service(**data)


@dataclass
class Host(DataClassMixin):
    services: Set[str]
    service_args: Dict[str, str]

    ip: str = ''
    env: str = ''
    user: str = ''
    port: int = 0

    @staticmethod
    def load(data: Dict, env):
        return Host(env=env, **data)

    @property
    def cxn(self):
        return Connection(self.ip, user=self.user, port=self.port)

    def run(self, *args, **kwargs):
        self.cxn.run(*args, **kwargs)


@dataclass
class Bigga(DataClassMixin):
    name: str
    version: str
    language: str
    description: str
    hosts: Dict[str, Set[Host]]
    services: Set[Service]

    @staticmethod
    def load(data: Dict):
        hosts = {}
        for env, _hosts in data["hosts"].items():
            hosts[env] = [Host.load(host, env) for host in _hosts]
        data['hosts'] = hosts
        data['services'] = [
            Service.load(service) for service in data['services']]
        return Bigga(**data)


def read_bigga():
    data = jload(open(BIGGA_JSON))
    return Bigga.load(data)
