from io import BytesIO

from docker import DockerClient
from docker.errors import NotFound

from dto.docker import Image, Container
from utils.singleton import Singleton
from utils.datetime_utils import int2date
from typing import Dict


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
        history["Created"] = int2date(history["Created"], to_string=True)
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

    def build_image(
        self,
        path: str = "",
        dockerfile: BytesIO = None,
        tag: str = "latest",
        dto: bool = False,
        json: bool = False,
    ):
        try:
            if path:
                image, build_logs = self.client.images.build(path=path, tag=tag)
            elif dockerfile:
                image, build_logs = self.client.images.build(
                    fileobj=dockerfile, tag=tag
                )
            else:
                return 400, False, "Dockerfile or path required"

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
