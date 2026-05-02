"""SentimentIQ - Event Model (MongoDB)"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Event(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    event_type: str
    name: str
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    estimated_impact: Optional[float] = None
    actual_impact: Optional[float] = None
    affected_products: Optional[str] = None
    affected_categories: Optional[str] = None
    source: Optional[str] = None
    external_link: Optional[str] = None
    status: str = "active"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    class Config:
        populate_by_name = True
