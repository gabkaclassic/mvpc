from docker import DockerClient
from docker.errors import ImageNotFound, NotFound, APIError
from dto.common.docker import Container
from utils.singleton import Singleton


class Containers(metaclass=Singleton):

    def __init__(self, client: DockerClient):
        self.client = client

    def containers_list(self, json: bool = False, dto: bool = False):
        try:
            containers = self.client.containers.list(all=True)

            if dto:
                containers = [
                    Container(id=c.short_id, name=c.name, status=c.status)
                    for c in containers
                ]
            elif json:
                containers = [
                    Container(id=c.short_id, name=c.name, status=c.status).json()
                    for c in containers
                ]

            return 200, True, containers
        except Exception as e:
            return 500, False, "Internal server error"

    def get_container(self, container_id: str, json: bool = False, dto: bool = False):
        try:
            container = self.client.containers.get(container_id)

            if dto:
                container = Container(
                    id=container.short_id, name=container.name, status=container.status
                )
            elif json:
                container = Container(
                    id=container.short_id, name=container.name, status=container.status
                ).json()

            return 200, True, container
        except NotFound as e:
            return e.status_code, False, f"Container {container_id} not found"
        except Exception as e:
            return 500, False, "Internal server error"

    def get_container_logs_stream(self, container_id: str):
        container = self.client.containers.get(container_id)
        for line in container.logs(stream=True, follow=True):
            yield line.decode("utf-8")

    def get_container_logs(self, container_id: str):
        try:
            container = self.client.containers.get(container_id)

            logs = container.logs()
            return 200, True, logs
        except NotFound as e:
            return e.status_code, False, f"Container {container_id} not found"
        except Exception as e:
            return 500, False, "Internal server error"

    def create_container(self, name: str, image: str, json: bool = False):
        try:
            created_container = self.client.containers.run(
                name=name, image=image, detach=True
            )
            if json:
                created_container = Container(
                    created_container.id,
                    created_container.name,
                    status=created_container.status,
                ).json()

            return created_container, True, "Container success created"
        except ImageNotFound as e:
            return e.status_code, False, f"Image {image} not found"
        except APIError as e:
            status_code = e.status_code
            return (
                status_code,
                False,
                (
                    f"Invalid name: {name}"
                    if status_code == 400
                    else f"Container with name {name} already exists"
                ),
            )

    def execute_command(self, container_id: str, command: str):
        container = self.client.containers.get(container_id)
        for result_line in container.exec_run(command, stream=True):
            if result_line:
                for line in result_line:
                    yield line.decode("utf-8")

    def remove_container(self, id: str, force: bool = False):

        try:
            container = self.client.containers.get(id)
            container_status = container.status

            if force and container_status == "running":
                container.stop()
                container.remove()
                return None, True, "Container successfully removed"
            elif container_status != "running":
                container.remove()
                return None, True, "Container successfully removed"

            return 400, False, "Container remove operation must be forced"

        except NotFound as e:
            return 404, False, f"Container with id {id} not found"
        except Exception as e:
            return 500, False, "Internal server error"

    def stop_container(self, id: str):

        try:
            container = self.client.containers.get(id)
            container_status = container.status
            result = None
            already_stopped = container_status == "exited"
            if not already_stopped:
                result = container.stop()

            return (
                result,
                True,
                (
                    "Container already stopped"
                    if already_stopped
                    else "Container successfully stopped"
                ),
            )

        except NotFound as e:
            return 404, False, f"Container with id {id} not found"
        except Exception as e:
            return 500, False, "Internal server error"
