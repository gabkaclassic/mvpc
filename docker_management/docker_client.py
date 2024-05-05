from docker import DockerClient
from utils.singleton import Singleton
from .containers import Containers


class Docker(metaclass=Singleton):

    def __init__(self):
        self.client = DockerClient("unix://var/run/docker.sock")
        self.containers = Containers(client=self.client)


client = Docker()
