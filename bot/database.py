import json
import os

from bson import decode_file_iter
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DB")]
collection = db[os.getenv("MONGO_COLLECTION")]


async def restore_collection_from_bson(bson_file_path: str) -> None:
    await collection.drop()

    with open(bson_file_path, "rb") as bson_file:
        for document in decode_file_iter(bson_file):
            await collection.insert_one(document)
        return


async def apply_metadata(metadata_file_path: str) -> None:
    with open(metadata_file_path, "r") as metadata_file:
        metadata = json.load(metadata_file)
        if "indexes" in metadata:
            for index in metadata["indexes"]:
                keys = list(index["key"].items())
                await collection.create_index(keys)
            return
