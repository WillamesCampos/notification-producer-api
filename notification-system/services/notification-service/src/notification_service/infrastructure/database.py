from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from notification_service.config import logger, settings


_client: Optional[AsyncIOMotorClient] = None
_db = None
_collection = None


async def init_database():
    global _client, _db, _collection

    logger.info("🔌 Connecting to MongoDB...")

    if _client is None:
        _client = AsyncIOMotorClient(settings.mongodb_uri)
        _db = _client[settings.mongodb_database]
        _collection = _db[settings.mongodb_collection]

    await _collection.create_index([("event_id", 1)], unique=True)
    await _collection.create_index([("user_id", 1), ("timestamp", -1)])

    logger.info("✅ Database initialized successfully")


async def close_database():
    global _client, _db, _collection

    logger.info("🔌 Closing MongoDB connection...")

    if _client is not None:
        _client.close()
        _client = None
        _db = None
        _collection = None

        logger.info("✅ Database connection closed successfully")


def get_collection():
    if _collection is None:
        raise RuntimeError("Database connection not initialized. Initialize the database first.")
    return _collection

