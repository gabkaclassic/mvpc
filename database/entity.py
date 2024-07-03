from abc import ABC
from uuid import uuid4


class Entity(ABC):

    required_fields = {"id"}

    id: str

    def __init__(self, dto):
        self.id = dto.id or uuid4()
