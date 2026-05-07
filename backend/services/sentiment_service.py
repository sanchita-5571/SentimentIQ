"""
SentimentIQ - Sentiment Service (MongoDB version)
"""

from datetime import datetime
from typing import List, Optional

from bson import ObjectId

from db.mongodb import get_mongodb
from db.postgres import REVIEWS_COLLECTION


class SentimentService:
    """Service for sentiment operations using MongoDB"""

    @staticmethod
    async def get_sentiment_by_id(sentiment_id: str) -> Optional[dict]:
        """Get sentiment result by ID"""
        db = get_mongodb()
        if db is None:
            return None

        try:

            return await db[REVIEWS_COLLECTION].find_one({"_id": ObjectId(sentiment_id)})
        except Exception:
            return None

    @staticmethod
    async def get_sentiments_for_review(review_id: str) -> List[dict]:
        """Get all sentiment results for a review"""
        db = get_mongodb()
        if db is None:
            return []

        try:
            doc = await db[REVIEWS_COLLECTION].find_one({"_id": ObjectId(review_id)})
            if doc:
                return [doc]
            return []
        except Exception:
            return []

    @staticmethod
    async def create_sentiment_result(review_id: str, sentiment_data: dict) -> dict:
        """Create a new sentiment result"""
        db = get_mongodb()
        if db is None:
            raise RuntimeError("MongoDB not connected")

        sentiment_data["updated_at"] = datetime.utcnow()

        await db[REVIEWS_COLLECTION].update_one(
            {"_id": ObjectId(review_id)},
            {"$set": sentiment_data}
        )

        return await db[REVIEWS_COLLECTION].find_one({"_id": ObjectId(review_id)})

    @staticmethod
    async def get_sentiment_stats(user_id: str) -> dict:
        """Get sentiment statistics"""
        db = get_mongodb()
        if db is None:
            return {
                "total_reviews": 0,
                "positive_count": 0,
                "negative_count": 0,
                "neutral_count": 0,
                "avg_sentiment": 0.0
            }

        query = {"user_id": user_id, "sentiment_score": {"$ne": None}}

        total = await db[REVIEWS_COLLECTION].count_documents(query)
        positive = await db[REVIEWS_COLLECTION].count_documents({**query, "sentiment_label": "positive"})
        negative = await db[REVIEWS_COLLECTION].count_documents({**query, "sentiment_label": "negative"})
        neutral = await db[REVIEWS_COLLECTION].count_documents({**query, "sentiment_label": "neutral"})

        cursor = db[REVIEWS_COLLECTION].find(query)
        reviews = await cursor.to_list(length=10000)
        avg_sentiment = sum(r.get("sentiment_score", 0) for r in reviews) / total if total > 0 else 0.0

        return {
            "total_reviews": total,
            "positive_count": positive,
            "negative_count": negative,
            "neutral_count": neutral,
            "avg_sentiment": avg_sentiment
        }
