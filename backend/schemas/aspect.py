"""
SentimentIQ - Aspect Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AspectBase(BaseModel):
    """Base aspect schema"""
    name: str
    category: Optional[str] = None
    avg_sentiment: Optional[float] = None
    positive_count: int = 0
    negative_count: int = 0
    neutral_count: int = 0
    total_mentions: int = 0
    confidence_threshold: float = 0.5
    is_active: bool = True


class AspectCreate(AspectBase):
    """Schema for creating an aspect"""
    pass


class AspectUpdate(BaseModel):
    """Schema for updating an aspect"""
    name: Optional[str] = None
    category: Optional[str] = None
    avg_sentiment: Optional[float] = None
    positive_count: Optional[int] = None
    negative_count: Optional[int] = None
    neutral_count: Optional[int] = None
    total_mentions: Optional[int] = None
    confidence_threshold: Optional[float] = None
    is_active: Optional[bool] = None


class Aspect(AspectBase):
    """Full aspect schema"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class ReviewAspectBase(BaseModel):
    """Base review-aspect relationship schema"""
    review_id: int
    aspect_id: int
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    confidence: Optional[float] = None
    start_char: Optional[int] = None
    end_char: Optional[int] = None
    aspect_text: Optional[str] = None


class ReviewAspectCreate(ReviewAspectBase):
    """Schema for creating a review-aspect relationship"""
    pass


class ReviewAspect(ReviewAspectBase):
    """Full review-aspect relationship schema"""
    model_config = ConfigDict(from_attributes=True)

    id: int