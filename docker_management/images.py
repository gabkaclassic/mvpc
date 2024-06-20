from docker import DockerClient
from docker.errors import NotFound

from dto.common.docker import Image, Container
from dto.controllers.image import Layer
from utils.common.singleton import Singleton
from utils.common.datetime_utils import int_to_date
from utils.docker.dockerfile import create_dockerfile
from typing import Dict
from fastapi import UploadFile as File
from os.path import join as path_join
from pathlib import Path
from uuid import uuid4
from setup import docker_work_directory as work_directory


class Images(metaclass=Singleton):

    def __init__(self, client: DockerClient):
        self.client = client

    def images_list(self, json: bool = False, dto: bool = False):
        try:
            images = self.client.images.list()
            if dto:
                images = [
                    Image(id=i.short_id, labels=i.labels, tags=i.tags) for i in images
                ]
            elif json:
                images = [
                    Image(id=i.short_id, labels=i.labels, tags=i.tags).json()
                    for i in images
                ]

            return 200, True, images
        except Exception as e:
            return 500, False, "Internal server error"

    def get_image_containers(self, image: str):
        return self.client.containers.list(all=True, filters={"ancestor": image})

    def format_history(self, history: Dict):
        history["Created"] = int_to_date(history["Created"], to_string=True)
        return history

    def get_image(self, image_name: str, json: bool = False, dto: bool = False):
        try:
            image = self.client.images.get(image_name)
            history = list(map(self.format_history, image.history()))
            containers = self.get_image_containers(image_name)
            if dto:
                containers = [
                    Container(id=c.id, name=c.name, status=c.status) for c in containers
                ]
                image = Image(
                    id=image.short_id,
                    labels=image.labels,
                    tags=image.tags,
                    history=history,
                    containers=containers,
                )
            elif json:
                containers = [
                    Container(id=c.id, name=c.name, status=c.status).json()
                    for c in containers
                ]
                image = Image(
                    id=image.short_id,
                    labels=image.labels,
                    tags=image.tags,
                    history=history,
                    containers=containers,
                ).json()

            return 200, True, image
        except Exception as e:
            print(e)
            return 500, False, "Internal server error"

    async def build_image(
        self,
        super_image: str,
        title: str,
        tag: str = "latest",
        layers: list[Layer] = None,
        files: list[File] = None,
        json: bool = False,
        dto: bool = False,
    ):
        try:

            layers = layers or []
            files = files or []

            dockerfile_content = create_dockerfile(
                super_image=super_image, layers=layers
            )

            build_directory = path_join(work_directory, str(uuid4())[-12:])
            Path(build_directory).mkdir(exist_ok=True, parents=True)
            dockerfile_path = path_join(build_directory, "Dockerfile")
            with open(dockerfile_path, "w+") as dockerfile:
                dockerfile.write(dockerfile_content)
            for file in files:
                file_path = path_join(build_directory, file.filename)
                with open(file_path, "wb") as image_file:
                    content = await file.read()
                    image_file.write(content)

            image, build_logs = self.client.images.build(
                # target=title,
                tag=f"{title}:{tag}",
                path=build_directory,
            )

            if dto:
                image = Image(id=image.short_id, labels=image.labels, tags=image.tags)
            elif json:
                image = Image(
                    id=image.short_id, labels=image.labels, tags=image.tags
                ).json()

            logs = "/n".join([l["stream"] for l in build_logs if "stream" in l])
            return 200, True, (image, logs)
        except Exception as e:
            return 500, False, "Internal server error"

    def pull_image(
        self, repository: str, tag: str, dto: bool = False, json: bool = False
    ):
        try:
            image = self.client.images.pull(repository=repository, tag=tag)

            if dto:
                image = Image(id=image.short_id, labels=image.labels, tags=image.tags)
            elif json:
                image = Image(
                    id=image.short_id, labels=image.labels, tags=image.tags
                ).json()

            return 200, True, image

        except NotFound as e:
            return e.status_code, False, "Image not found"
        except Exception as e:
            return 500, False, "Internal server error"

    def remove_image(self, image: str, force: bool = False, pruned: bool = False):
        try:
            self.client.images.remove(image, force=force, noprune=not pruned)
            return 200, True, "Success removing image"
        except NotFound as e:
            return e.status_code, False, "Image not found"
        except Exception as e:
            return 500, False, "Internal server error"
