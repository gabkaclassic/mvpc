from dataclasses import dataclass


@dataclass
class Container:
    id: str
    name: str
    status: str

    def json(self):
        return self.__dict__
