from motor.motor_asyncio import AsyncIOMotorClient

from setup import db_host, db_name, db_password, db_port, db_username
from utils.common import singleton


class MongoClient(metaclass=singleton):
    def __init__(self, username: str, password: str, host: str, port: str, name: str):
        connection_string = f"mongodb://{username}:{password}@{host}:{port}/{name}"
        self.client = AsyncIOMotorClient(connection_string)
        self.connection = self.client.get_database(name)

    def get_collection(self, collection: str):
        try:
            return self.connection.get_collection(collection)
        except Exception as e:
            print(e)
            return None


client = MongoClient(db_username, db_password, db_host, db_name, db_port)
