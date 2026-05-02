"""
SentimentIQ - Review Service (MongoDB version)
"""

from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel

from db.mongodb import get_mongodb
from db.postgres import REVIEWS_COLLECTION


class ReviewService:
    """Service for review operations using MongoDB"""

    @staticmethod
    async def get_review_by_id(review_id: str, user_id: str) -> Optional[dict]:
        """Get review by ID"""
        db = get_mongodb()
        if db is None:
            return None

        try:
            return await db[REVIEWS_COLLECTION].find_one({"_id": ObjectId(review_id), "user_id": user_id})
        except Exception:
            return None

    @staticmethod
    async def get_reviews(user_id: str, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all reviews with pagination"""
        db = get_mongodb()
        if db is None:
            return []

        cursor = db[REVIEWS_COLLECTION].find({"user_id": user_id}).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    @staticmethod
    async def create_review(user_id: str, review_data: dict) -> dict:
        """Create a new review"""
        db = get_mongodb()
        if db is None:
            raise RuntimeError("MongoDB not connected")

        # Calculate word count and char count
        content = review_data.get("content", "")
        word_count = len(content.split())
        char_count = len(content)

        review_doc = {
            **review_data,
            "user_id": user_id,
            "word_count": word_count,
            "char_count": char_count,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        result = await db[REVIEWS_COLLECTION].insert_one(review_doc)
        review_doc["_id"] = result.inserted_id
        return review_doc

    @staticmethod
    async def update_review(review_id: str, user_id: str, review_data: dict) -> Optional[dict]:
        """Update an existing review"""
        db = get_mongodb()
        if db is None:
            return None

        update_data = {k: v for k, v in review_data.items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()

        await db[REVIEWS_COLLECTION].update_one(
            {"_id": ObjectId(review_id), "user_id": user_id},
            {"$set": update_data}
        )

        return await db[REVIEWS_COLLECTION].find_one({"_id": ObjectId(review_id)})

    @staticmethod
    async def delete_review(review_id: str, user_id: str) -> bool:
        """Delete a review"""
        db = get_mongodb()
        if db is None:
            return False

        result = await db[REVIEWS_COLLECTION].delete_one({"_id": ObjectId(review_id), "user_id": user_id})
        return result.deleted_count > 0
