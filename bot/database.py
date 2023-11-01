import json

import motor.motor_asyncio
from aiofiles import os
from bson import decode_file_iter

load_dotenv()

async def restore_collection_from_bson(db, bson_file_path):
    collection = db[os.getenv("MONGO_DB")]
    await collection.drop()

    with open(bson_file_path, 'rb') as bson_file:
        for document in decode_file_iter(bson_file):
            await collection.insert_one(document)


async def apply_metadata(db, metadata_file_path):
    collection = db[os.getenv("MONGO_DB")]
    with open(metadata_file_path, 'r') as metadata_file:
        metadata = json.load(metadata_file)
        if 'indexes' in metadata:
            for index in metadata['indexes']:
                await collection.create_index(index['key'], **index['options'])
