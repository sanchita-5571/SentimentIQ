"""
SentimentIQ - Brand Service (MongoDB version)
"""

from datetime import datetime
from typing import List, Optional

from bson import ObjectId

from db.mongodb import get_mongodb
from db.postgres import BRANDS_COLLECTION


class BrandService:
    """Service for brand operations using MongoDB"""

    @staticmethod
    async def get_brand_by_id(brand_id: str) -> Optional[dict]:
        """Get brand by ID"""
        db = get_mongodb()
        if db is None:
            return None

        try:
            return await db[BRANDS_COLLECTION].find_one({"_id": ObjectId(brand_id)})
        except Exception:
            return None

    @staticmethod
    async def get_brands(skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all brands with pagination"""
        db = get_mongodb()
        if db is None:
            return []

        cursor = db[BRANDS_COLLECTION].find().skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    @staticmethod
    async def create_brand(brand_data: dict) -> dict:
        """Create a new brand"""
        db = get_mongodb()
        if db is None:
            raise RuntimeError("MongoDB not connected")

        brand_doc = {
            **brand_data,
            "is_active": brand_data.get("is_active", True),
            "sentiment_threshold": brand_data.get("sentiment_threshold", 0.05),
            "anomaly_threshold": brand_data.get("anomaly_threshold", 0.3),
            "spam_threshold": brand_data.get("spam_threshold", 0.8),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        result = await db[BRANDS_COLLECTION].insert_one(brand_doc)
        brand_doc["_id"] = result.inserted_id
        return brand_doc

    @staticmethod
    async def update_brand(brand_id: str, brand_data: dict) -> Optional[dict]:
        """Update an existing brand"""
        db = get_mongodb()
        if db is None:
            return None

        update_data = {k: v for k, v in brand_data.items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()

        await db[BRANDS_COLLECTION].update_one(
            {"_id": ObjectId(brand_id)},
            {"$set": update_data}
        )

        return await db[BRANDS_COLLECTION].find_one({"_id": ObjectId(brand_id)})

    @staticmethod
    async def delete_brand(brand_id: str) -> bool:
        """Delete a brand"""
        db = get_mongodb()
        if db is None:
            return False

        result = await db[BRANDS_COLLECTION].delete_one({"_id": ObjectId(brand_id)})
        return result.deleted_count > 0

    @staticmethod
    async def get_brands_by_industry(industry: str, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get brands by industry"""
        db = get_mongodb()
        if db is None:
            return []

        cursor = db[BRANDS_COLLECTION].find({"industry": industry}).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
