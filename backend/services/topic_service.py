"""
SentimentIQ - Topic Service (MongoDB version)
"""

from datetime import datetime
from typing import List, Optional

from bson import ObjectId

from db.mongodb import get_mongodb
from db.postgres import TOPICS_COLLECTION


class TopicService:
    """Service for topic operations using MongoDB"""

    @staticmethod
    async def get_topic_by_id(topic_id: str) -> Optional[dict]:
        """Get topic by ID"""
        db = get_mongodb()
        if db is None:
            return None

        try:
            return await db[TOPICS_COLLECTION].find_one({"_id": ObjectId(topic_id)})
        except Exception:
            return None

    @staticmethod
    async def get_topics(skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all topics with pagination"""
        db = get_mongodb()
        if db is None:
            return []

        cursor = db[TOPICS_COLLECTION].find().skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    @staticmethod
    async def create_topic(topic_data: dict) -> dict:
        """Create a new topic"""
        db = get_mongodb()
        if db is None:
            raise RuntimeError("MongoDB not connected")

        topic_doc = {
            **topic_data,
            "is_active": topic_data.get("is_active", True),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        result = await db[TOPICS_COLLECTION].insert_one(topic_doc)
        topic_doc["_id"] = result.inserted_id
        return topic_doc

    @staticmethod
    async def update_topic(topic_id: str, topic_data: dict) -> Optional[dict]:
        """Update an existing topic"""
        db = get_mongodb()
        if db is None:
            return None

        update_data = {k: v for k, v in topic_data.items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()

        await db[TOPICS_COLLECTION].update_one(
            {"_id": ObjectId(topic_id)},
            {"$set": update_data}
        )

        return await db[TOPICS_COLLECTION].find_one({"_id": ObjectId(topic_id)})

    @staticmethod
    async def delete_topic(topic_id: str) -> bool:
        """Delete a topic"""
        db = get_mongodb()
        if db is None:
            return False

        result = await db[TOPICS_COLLECTION].delete_one({"_id": ObjectId(topic_id)})
        return result.deleted_count > 0

    @staticmethod
    async def get_topics_by_cluster(cluster: str, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get topics by cluster"""
        db = get_mongodb()
        if db is None:
            return []

        cursor = db[TOPICS_COLLECTION].find({"cluster": cluster}).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
