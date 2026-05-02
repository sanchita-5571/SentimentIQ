"""
SentimentIQ - Anomaly Service (MongoDB version)
"""

from datetime import datetime
from typing import List, Optional

from bson import ObjectId

from db.mongodb import get_mongodb
from db.postgres import ANOMALIES_COLLECTION


class AnomalyService:
    """Service for anomaly operations using MongoDB"""

    @staticmethod
    async def get_anomaly_by_id(anomaly_id: str) -> Optional[dict]:
        """Get anomaly by ID"""
        db = get_mongodb()
        if db is None:
            return None

        try:
            return await db[ANOMALIES_COLLECTION].find_one({"_id": ObjectId(anomaly_id)})
        except Exception:
            return None

    @staticmethod
    async def get_anomalies(skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all anomalies with pagination"""
        db = get_mongodb()
        if db is None:
            return []

        cursor = db[ANOMALIES_COLLECTION].find().skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    @staticmethod
    async def create_anomaly(anomaly_data: dict) -> dict:
        """Create a new anomaly"""
        db = get_mongodb()
        if db is None:
            raise RuntimeError("MongoDB not connected")

        anomaly_doc = {
            **anomaly_data,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        result = await db[ANOMALIES_COLLECTION].insert_one(anomaly_doc)
        anomaly_doc["_id"] = result.inserted_id
        return anomaly_doc

    @staticmethod
    async def update_anomaly(anomaly_id: str, anomaly_data: dict) -> Optional[dict]:
        """Update an existing anomaly"""
        db = get_mongodb()
        if db is None:
            return None

        update_data = {k: v for k, v in anomaly_data.items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()

        await db[ANOMALIES_COLLECTION].update_one(
            {"_id": ObjectId(anomaly_id)},
            {"$set": update_data}
        )

        return await db[ANOMALIES_COLLECTION].find_one({"_id": ObjectId(anomaly_id)})

    @staticmethod
    async def delete_anomaly(anomaly_id: str) -> bool:
        """Delete an anomaly"""
        db = get_mongodb()
        if db is None:
            return False

        result = await db[ANOMALIES_COLLECTION].delete_one({"_id": ObjectId(anomaly_id)})
        return result.deleted_count > 0
