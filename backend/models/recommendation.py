"""SentimentIQ - Recommendation Model (MongoDB)"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Recommendation(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    impact_score: Optional[float] = None
    confidence_score: Optional[float] = None
    source_type: Optional[str] = None
    source_id: Optional[str] = None
    status: str = "pending"
    implemented_at: Optional[datetime] = None
    dismissed_at: Optional[datetime] = None
    dismissed_reason: Optional[str] = None
    root_cause_id: Optional[str] = None
    anomaly_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    class Config:
        populate_by_name = True