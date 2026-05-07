"""
SentimentIQ - Anomaly Model
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class Anomaly(BaseModel):
    """MongoDB Anomaly model - detected sentiment drops"""
    
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str

    anomaly_type: str  # sentiment_drop, volume_spike, etc.
    severity: str  # low, medium, high, critical
    title: str
    description: Optional[str] = None

    baseline_score: Optional[float] = None  # Historical average
    current_score: Optional[float] = None  # Current value
    deviation: Optional[float] = None  # Difference from baseline
    deviation_percentage: Optional[float] = None

    start_date: datetime
    end_date: Optional[datetime] = None
    duration_minutes: Optional[int] = None

    affected_reviews: Optional[int] = None  # Count of affected reviews
    affected_products: Optional[str] = None  # JSON list of affected products
    affected_categories: Optional[str] = None  # JSON list of affected categories

    status: str = "detected"  # detected, investigating, resolved, dismissed
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None

    detected_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True


class AnomalyTrigger(BaseModel):
    """MongoDB Anomaly Trigger - reviews that triggered an anomaly"""
    
    id: Optional[str] = Field(default=None, alias="_id")
    anomaly_id: str
    review_id: str

    trigger_type: str  # low_rating, negative_sentiment, etc.
    contribution_score: Optional[float] = None  # How much this review contributed
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
