from dataclasses import dataclass
from typing import List


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
    containers: List = None
    history: List = None

    def json(self):
        return self.__dict__
