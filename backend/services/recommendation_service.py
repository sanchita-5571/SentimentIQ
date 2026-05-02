"""
SentimentIQ - Recommendation Service (MongoDB version)
"""

from datetime import datetime
from typing import List, Optional

from bson import ObjectId

from db.mongodb import get_mongodb
from db.postgres import RECOMMENDATIONS_COLLECTION


class RecommendationService:
    """Service for recommendation operations using MongoDB"""

    @staticmethod
    async def get_recommendation_by_id(recommendation_id: str) -> Optional[dict]:
        """Get recommendation by ID"""
        db = get_mongodb()
        if db is None:
            return None

        try:
            return await db[RECOMMENDATIONS_COLLECTION].find_one({"_id": ObjectId(recommendation_id)})
        except Exception:
            return None

    @staticmethod
    async def get_recommendations(skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all recommendations with pagination"""
        db = get_mongodb()
        if db is None:
            return []

        cursor = db[RECOMMENDATIONS_COLLECTION].find().skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    @staticmethod
    async def create_recommendation(recommendation_data: dict) -> dict:
        """Create a new recommendation"""
        db = get_mongodb()
        if db is None:
            raise RuntimeError("MongoDB not connected")

        recommendation_doc = {
            **recommendation_data,
            "status": recommendation_data.get("status", "pending"),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        result = await db[RECOMMENDATIONS_COLLECTION].insert_one(recommendation_doc)
        recommendation_doc["_id"] = result.inserted_id
        return recommendation_doc

    @staticmethod
    async def update_recommendation(recommendation_id: str, recommendation_data: dict) -> Optional[dict]:
        """Update an existing recommendation"""
        db = get_mongodb()
        if db is None:
            return None

        update_data = {k: v for k, v in recommendation_data.items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()

        await db[RECOMMENDATIONS_COLLECTION].update_one(
            {"_id": ObjectId(recommendation_id)},
            {"$set": update_data}
        )

        return await db[RECOMMENDATIONS_COLLECTION].find_one({"_id": ObjectId(recommendation_id)})

    @staticmethod
    async def delete_recommendation(recommendation_id: str) -> bool:
        """Delete a recommendation"""
        db = get_mongodb()
        if db is None:
            return False

        result = await db[RECOMMENDATIONS_COLLECTION].delete_one({"_id": ObjectId(recommendation_id)})
        return result.deleted_count > 0

    @staticmethod
    async def get_recommendations_by_status(status: str, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get recommendations by status"""
        db = get_mongodb()
        if db is None:
            return []

        cursor = db[RECOMMENDATIONS_COLLECTION].find({"status": status}).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    @staticmethod
    async def get_recommendations_by_priority(priority: str, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get recommendations by priority"""
        db = get_mongodb()
        if db is None:
            return []

        cursor = db[RECOMMENDATIONS_COLLECTION].find({"priority": priority}).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
