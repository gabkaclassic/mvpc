from abc import ABC
from uuid import uuid4


class Entity(ABC):
    id: str

    def __init__(self, id: str = None):
        self.id = id or uuid4()
