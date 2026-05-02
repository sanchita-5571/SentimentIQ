"""
SentimentIQ - Topic Schemas
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class TopicBase(BaseModel):
    """Base topic schema"""
    name: str
    keywords: Optional[str] = None
    description: Optional[str] = None
    topic_id: int
    probability: Optional[float] = None
    count: int = 0
    avg_sentiment: Optional[float] = None
    positive_count: int = 0
    negative_count: int = 0
    neutral_count: int = 0


class TopicCreate(TopicBase):
    """Schema for creating a topic"""
    pass


class TopicUpdate(BaseModel):
    """Schema for updating a topic"""
    name: Optional[str] = None
    keywords: Optional[str] = None
    description: Optional[str] = None
    probability: Optional[float] = None
    count: Optional[int] = None
    avg_sentiment: Optional[float] = None
    positive_count: Optional[int] = None
    negative_count: Optional[int] = None
    neutral_count: Optional[int] = None


class Topic(TopicBase):
    """Full topic schema"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class ReviewTopicBase(BaseModel):
    """Base review-topic relationship schema"""
    review_id: int
    topic_id: int
    probability: Optional[float] = None


class ReviewTopicCreate(ReviewTopicBase):
    """Schema for creating a review-topic relationship"""
    pass


class ReviewTopic(ReviewTopicBase):
    """Full review-topic relationship schema"""
    model_config = ConfigDict(from_attributes=True)

    id: int