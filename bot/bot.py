import asyncio
import logging
import os

import motor

import handlers
from loader import bot, db, dp

load_dotenv()
logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot")

    client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URI"))
    db = client[os.getenv("MONGO_DB")]

    # Paths to your BSON and JSON files
    bson_file_path = './data/sample_collection.bson'
    metadata_file_path = './data/sample_collections.metadata.json'

    logger.info("Database is created")

    dp.include_router(handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())