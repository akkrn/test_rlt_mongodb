import json

from bson import decode_file_iter
from dotenv import load_dotenv
from motor.core import AgnosticCollection

load_dotenv()


async def restore_collection_from_bson(
    collection: AgnosticCollection, bson_file_path: str
) -> None:
    await collection.drop()

    with open(bson_file_path, "rb") as bson_file:
        for document in decode_file_iter(bson_file):
            await collection.insert_one(document)


async def apply_metadata(
    collection: AgnosticCollection, metadata_file_path: str
) -> None:
    with open(metadata_file_path, "r") as metadata_file:
        metadata = json.load(metadata_file)
        if "indexes" in metadata:
            for index in metadata["indexes"]:
                await collection.create_index(index["key"], **index["options"])
