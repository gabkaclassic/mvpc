from enum import Enum

from fastapi import Form
from fastapi import UploadFile as File
from pydantic import BaseModel as Model


class DockerfileInstruction(Enum):
    FROM = "FROM"
    RUN = "RUN"
    ADD = "ADD"
    ARG = "ARG"
    CMD = "CMD"
    COPY = "COPY"
    ENTRYPOINT = "ENTRYPOINT"
    EXPOSE = "EXPOSE"
    ENV = "ENV"
    LABEL = "LABEL"
    HEALTHCHECK = "HEALTHCHECK"
    MAINTAINER = "MAINTAINER"
    ONBUILD = "ONBUILD"
    SHELL = "SHELL"
    USER = "USER"
    VOLUME = "VOLUME"
    WORKDIR = "WORKDIR"
    STOPSIGNAL = "STOPOSIGNAL"


class Layer(Model):
    instruction: DockerfileInstruction
    command_arguments: list[str]
    description: str | None


class CreateImage(Model):
    super_image: str
    title: str
    tag: str
    layers: str
    files: list[File]

    @classmethod
    def as_form(
        cls,
        super_image: str = Form(...),
        title: str = Form(...),
        tag: str = Form(...),
        layers: str = Form(...),
        files: list[File] = File(...),
    ) -> "CreateImage":
        return cls(super_image=super_image, title=title, tag=tag, layers=layers, files=files)


class PullImage(Model):
    repository: str
    tag: str


class RemoveImage(Model):
    image: str
    force: bool = False
    pruned: bool = False
