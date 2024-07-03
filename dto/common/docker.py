from dataclasses import dataclass


@dataclass
class Container:
    id: str
    name: str
    status: str

    def json(self):
        return self.__dict__


@dataclass
class Image:
    id: str
    labels: str
    tags: str
    containers: list = None
    history: list = None

    def json(self):
        return self.__dict__
