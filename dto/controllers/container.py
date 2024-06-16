from pydantic import BaseModel as Model


class CreateContainer(Model):
    name: str
    image: str


class StopContainer(Model):
    id: str


class RemoveContainer(Model):
    id: str
    force: bool = False
