from typing import List

from database.connection import client
from database.entity import Entity


class Image(Entity):
    collection = client.get_collection("images")

    labels: str
    tag: str
    containers: List
    history: List

    def __init__(
        self,
        id: str = None,
        labels: str = "",
        tag: str = "",
        containers: List = None,
        history: List = None,
    ):
        super().__init__(id)
        self.labels = labels
        self.tag = tag
        self.containers = containers or []
        self.history = history or []

    def save(self):
        return self.collection.insert_one(self.__dict__)

    def delete(self):
        return self.collection.delete_one(self.__dict__)

    def json(self):
        return self.__dict__

    def __dict__(self):
        return {
            "id": self.id,
            "labels": self.labels,
            "tag": self.tag,
            "containers": self.containers,
            "history": self.history,
        }
