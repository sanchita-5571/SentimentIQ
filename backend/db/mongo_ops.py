"""
MongoDB Database Operations for FastAPI
All database operations use MongoDB only.
Uses Motor for async MongoDB operations.

NOTE: This file was previously for PostgreSQL but has been refactored to use MongoDB.
The file name 'postgres.py' is kept for backward compatibility.
"""

from typing import Any, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from db.mongodb import get_mongodb


async def get_db_session() -> AsyncIOMotorDatabase:
    """Get MongoDB database instance for dependency injection"""
    db = get_mongodb()
    if db is None:
        raise RuntimeError("MongoDB is not connected. Please ensure MongoDB is running.")
    return db

db_session = get_db_session

USERS_COLLECTION = "users"
REVIEWS_COLLECTION = "reviews"
EVENTS_COLLECTION = "events"
SETTINGS_COLLECTION = "settings"
INGESTION_BATCHES_COLLECTION = "ingestion_batches"
BRANDS_COLLECTION = "brands"
ASPECTS_COLLECTION = "aspects"
TOPICS_COLLECTION = "topics"
ALERTS_COLLECTION = "alerts"
ANOMALIES_COLLECTION = "anomalies"
RECOMMENDATIONS_COLLECTION = "recommendations"


async def get_collection(name: str):
    """Get a MongoDB collection by name"""
    db = get_mongodb()
    if db is None:
        raise RuntimeError("MongoDB is not connected. Please ensure MongoDB is running.")
    return db[name]


async def find_one(collection: str, query: dict) -> Optional[dict]:
    """Find a single document"""
    db = await get_db_session()
    return await db[collection].find_one(query)


async def find_many(collection: str, query: dict, skip: int = 0, limit: int = 100, sort: list = None) -> list:
    """Find multiple documents"""
    db = await get_db_session()
    cursor = db[collection].find(query).skip(skip).limit(limit)
    if sort:
        cursor = cursor.sort(sort)
    return await cursor.to_list(length=limit)


async def insert_one(collection: str, document: dict) -> str:
    """Insert a single document and return its ID"""
    db = await get_db_session()
    result = await db[collection].insert_one(document)
    return str(result.inserted_id)


async def insert_many(collection: str, documents: list) -> list:
    """Insert multiple documents and return their IDs"""
    db = await get_db_session()
    result = await db[collection].insert_many(documents)
    return [str(id) for id in result.inserted_ids]


async def update_one(collection: str, query: dict, update: dict, upsert: bool = False) -> bool:
    """Update a single document"""
    db = await get_db_session()
    result = await db[collection].update_one(query, update, upsert=upsert)
    return result.modified_count > 0


async def update_many(collection: str, query: dict, update: dict) -> int:
    """Update multiple documents"""
    db = await get_db_session()
    result = await db[collection].update_many(query, update)
    return result.modified_count


async def delete_one(collection: str, query: dict) -> bool:
    """Delete a single document"""
    db = await get_db_session()
    result = await db[collection].delete_one(query)
    return result.deleted_count > 0


async def delete_many(collection: str, query: dict) -> int:
    """Delete multiple documents"""
    db = await get_db_session()
    result = await db[collection].delete_many(query)
    return result.deleted_count


async def count_documents(collection: str, query: dict = {}) -> int:
    """Count documents in a collection"""
    db = await get_db_session()
    return await db[collection].count_documents(query)

