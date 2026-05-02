"""
MongoDB Base Models and Collections
"""

from typing import Any, Optional
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorDatabase
from db.mongodb import get_mongodb


async def get_db_session() -> AsyncIOMotorDatabase:
    """Get MongoDB database instance for dependency injection"""
    db = get_mongodb()
    if db is None:
        raise RuntimeError("MongoDB is not connected. Please ensure MongoDB is running.")
    return db


class MongoBaseModel:
    """Base class for MongoDB models with common fields"""
    
    collection_name: str = None
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self) -> dict:
        """Convert model to dictionary for MongoDB storage"""
        data = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                data[key] = value
        return data
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create model instance from MongoDB document"""
        return cls(**data)
