from docker import DockerClient
from utils.singleton import Singleton
from .containers import Containers
from .images import Images


class Docker(metaclass=Singleton):

    def __init__(self):
        self.client = DockerClient("unix://var/run/docker.sock")
        self.containers = Containers(client=self.client)
        self.images = Images(client=self.client)


client = Docker()
