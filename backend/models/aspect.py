"""
SentimentIQ - Aspect Model
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Aspect(BaseModel):
    """MongoDB Aspect model for aspect-based sentiment analysis"""

    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    category: Optional[str] = None  # e.g., product, service, delivery

    # Sentiment aggregation
    avg_sentiment: Optional[float] = None
    positive_count: int = 0
    negative_count: int = 0
    neutral_count: int = 0
    total_mentions: int = 0

    # Metadata
    confidence_threshold: float = 0.5
    is_active: bool = True

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True


class ReviewAspect(BaseModel):
    """MongoDB Many-to-many relationship between reviews and aspects with sentiment"""

    id: Optional[str] = Field(default=None, alias="_id")
    review_id: str
    aspect_id: str

    # Aspect sentiment for this review
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None  # positive, negative, neutral
    confidence: Optional[float] = None

    # Text span information
    start_char: Optional[int] = None
    end_char: Optional[int] = None
    aspect_text: Optional[str] = None  # The actual text span

    class Config:
        populate_by_name = True