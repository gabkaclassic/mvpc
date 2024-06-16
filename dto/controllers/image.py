from pydantic import BaseModel as Model
from fastapi import UploadFile


class Layer(Model):
    command: str
    description: str | None


class CreateImage(Model):
    title: str
    tag: str = "latest"
    layers: list[Layer]
    files: list[UploadFile]


class PullImage(Model):
    repository: str
    tag: str


class RemoveImage(Model):
    image: str
    force: bool = False
    pruned: bool = False
