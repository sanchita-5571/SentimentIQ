"""
SentimentIQ - Aspect Service (MongoDB version)
"""

from datetime import datetime
from typing import List, Optional

from bson import ObjectId

from db.mongodb import get_mongodb
from db.postgres import ASPECTS_COLLECTION


class AspectService:
    """Service for aspect operations using MongoDB"""

    @staticmethod
    async def get_aspect_by_id(aspect_id: str) -> Optional[dict]:
        """Get aspect by ID"""
        db = get_mongodb()
        if db is None:
            return None

        try:
            return await db[ASPECTS_COLLECTION].find_one({"_id": ObjectId(aspect_id)})
        except Exception:
            return None

    @staticmethod
    async def get_aspects(skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all aspects with pagination"""
        db = get_mongodb()
        if db is None:
            return []

        cursor = db[ASPECTS_COLLECTION].find().skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    @staticmethod
    async def create_aspect(aspect_data: dict) -> dict:
        """Create a new aspect"""
        db = get_mongodb()
        if db is None:
            raise RuntimeError("MongoDB not connected")

        aspect_doc = {
            **aspect_data,
            "is_active": aspect_data.get("is_active", True),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        result = await db[ASPECTS_COLLECTION].insert_one(aspect_doc)
        aspect_doc["_id"] = result.inserted_id
        return aspect_doc

    @staticmethod
    async def update_aspect(aspect_id: str, aspect_data: dict) -> Optional[dict]:
        """Update an existing aspect"""
        db = get_mongodb()
        if db is None:
            return None

        update_data = {k: v for k, v in aspect_data.items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()

        await db[ASPECTS_COLLECTION].update_one(
            {"_id": ObjectId(aspect_id)},
            {"$set": update_data}
        )

        return await db[ASPECTS_COLLECTION].find_one({"_id": ObjectId(aspect_id)})

    @staticmethod
    async def delete_aspect(aspect_id: str) -> bool:
        """Delete an aspect"""
        db = get_mongodb()
        if db is None:
            return False

        result = await db[ASPECTS_COLLECTION].delete_one({"_id": ObjectId(aspect_id)})
        return result.deleted_count > 0

    @staticmethod
    async def get_aspects_by_category(category: str, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get aspects by category"""
        db = get_mongodb()
        if db is None:
            return []

        cursor = db[ASPECTS_COLLECTION].find({"category": category}).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
