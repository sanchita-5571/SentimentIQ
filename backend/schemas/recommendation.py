"""
SentimentIQ - Recommendation Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RecommendationBase(BaseModel):
    """Base recommendation schema"""
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    impact_score: Optional[float] = None
    confidence_score: Optional[float] = None
    source_type: Optional[str] = None
    source_id: Optional[int] = None
    status: str = "pending"
    root_cause_id: Optional[int] = None
    anomaly_id: Optional[int] = None


class RecommendationCreate(RecommendationBase):
    """Schema for creating a recommendation"""
    pass


class RecommendationUpdate(BaseModel):
    """Schema for updating a recommendation"""
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    impact_score: Optional[float] = None
    confidence_score: Optional[float] = None
    status: Optional[str] = None
    implemented_at: Optional[datetime] = None
    dismissed_at: Optional[datetime] = None
    dismissed_reason: Optional[str] = None


class Recommendation(RecommendationBase):
    """Full recommendation schema"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    implemented_at: Optional[datetime] = None
    dismissed_at: Optional[datetime] = None
    dismissed_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime