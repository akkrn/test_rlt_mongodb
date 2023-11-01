import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

import handlers
from bot.database import apply_metadata, restore_collection_from_bson

load_dotenv()
logger = logging.getLogger(__name__)
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot")

    client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    db = client[os.getenv("MONGO_DB")]
    collection = db[os.getenv("MONGO_COLLECTION")]
    bson_file_path = "./data/sample_collection.bson"
    metadata_file_path = "./data/sample_collections.metadata.json"
    await restore_collection_from_bson(collection, bson_file_path)
    await apply_metadata(collection, metadata_file_path)
    logger.info("Database is ready")

    dp.include_router(handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
