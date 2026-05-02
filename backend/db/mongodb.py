from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from core.config import settings


mongo_client: AsyncIOMotorClient | None = None
mongo_db: AsyncIOMotorDatabase | None = None


async def init_mongodb() -> AsyncIOMotorDatabase | None:
    global mongo_client, mongo_db
    try:
        mongo_client = AsyncIOMotorClient(settings.MONGODB_URL, serverSelectionTimeoutMS=3000)
        await mongo_client.admin.command("ping")
        mongo_db = mongo_client[settings.MONGODB_NAME]
        await mongo_db.ingestion_batches.create_index("created_at")
        await mongo_db.report_exports.create_index("created_at")
        return mongo_db
    except Exception:
        mongo_client = None
        mongo_db = None
        return None


def get_mongodb() -> AsyncIOMotorDatabase | None:
    return mongo_db


async def close_mongodb() -> None:
    global mongo_client, mongo_db
    if mongo_client is not None:
        mongo_client.close()
    mongo_client = None
    mongo_db = None
