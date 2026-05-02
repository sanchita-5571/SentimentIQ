"""SentimentIQ - Root Cause Model (MongoDB)"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class RootCauseEvent(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    event_date: datetime
    baseline_sentiment: float
    current_sentiment: float
    sentiment_delta: float
    review_volume: int = 0
    earliest_degrading_aspect: Optional[str] = None
    amplification_chain: List[dict] = Field(default_factory=list)
    recommendations: List[dict] = Field(default_factory=list)
    evidence: List[dict] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    class Config:
        populate_by_name = True

class RootCause(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    anomaly_id: str
    event_id: Optional[str] = None
    root_cause_type: str
    description: Optional[str] = None
    confidence: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    class Config:
        populate_by_name = True
