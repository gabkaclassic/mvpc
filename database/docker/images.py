from database.connection import client
from database.entity import Entity
from dto.common.docker import Image as ImageDTO


class Image(Entity):
    collection = client.get_collection("images")

    def __init__(self, image: ImageDTO):
        super().__init__(image)

        for k, v in image.__dict__.items():
            self.__setattr__(k, v)

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
