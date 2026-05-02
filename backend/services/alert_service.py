"""
SentimentIQ - Alert Service (MongoDB version)
"""

from datetime import datetime
from typing import List, Optional

from bson import ObjectId

from db.mongodb import get_mongodb
from db.postgres import ALERTS_COLLECTION


class AlertService:
    """Service for alert operations using MongoDB"""

    @staticmethod
    async def get_alert_by_id(alert_id: str) -> Optional[dict]:
        """Get alert by ID"""
        db = get_mongodb()
        if db is None:
            return None

        try:
            return await db[ALERTS_COLLECTION].find_one({"_id": ObjectId(alert_id)})
        except Exception:
            return None

    @staticmethod
    async def get_alerts(skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all alerts with pagination"""
        db = get_mongodb()
        if db is None:
            return []

        cursor = db[ALERTS_COLLECTION].find().skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    @staticmethod
    async def create_alert(alert_data: dict) -> dict:
        """Create a new alert"""
        db = get_mongodb()
        if db is None:
            raise RuntimeError("MongoDB not connected")

        alert_doc = {
            **alert_data,
            "status": alert_data.get("status", "active"),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        result = await db[ALERTS_COLLECTION].insert_one(alert_doc)
        alert_doc["_id"] = result.inserted_id
        return alert_doc

    @staticmethod
    async def update_alert(alert_id: str, alert_data: dict) -> Optional[dict]:
        """Update an existing alert"""
        db = get_mongodb()
        if db is None:
            return None

        update_data = {k: v for k, v in alert_data.items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()

        await db[ALERTS_COLLECTION].update_one(
            {"_id": ObjectId(alert_id)},
            {"$set": update_data}
        )

        return await db[ALERTS_COLLECTION].find_one({"_id": ObjectId(alert_id)})

    @staticmethod
    async def delete_alert(alert_id: str) -> bool:
        """Delete an alert"""
        db = get_mongodb()
        if db is None:
            return False

        result = await db[ALERTS_COLLECTION].delete_one({"_id": ObjectId(alert_id)})
        return result.deleted_count > 0

    @staticmethod
    async def get_alerts_by_status(status: str, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get alerts by status"""
        db = get_mongodb()
        if db is None:
            return []

        cursor = db[ALERTS_COLLECTION].find({"status": status}).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    @staticmethod
    async def get_alerts_by_type(alert_type: str, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get alerts by type"""
        db = get_mongodb()
        if db is None:
            return []

        cursor = db[ALERTS_COLLECTION].find({"alert_type": alert_type}).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
