from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class Review(BaseModel):
    """MongoDB Review model"""
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    source: str
    external_id: Optional[str] = None
    author: Optional[str] = None
    title: Optional[str] = None
    content: str
    cleaned_text: str
    language: str = "unknown"
    rating: Optional[float] = None
    product: Optional[str] = None
    category: Optional[str] = None
    review_date: datetime
    normalized_hash: str
    is_duplicate: bool = False
    sentiment_score: float = 0.0
    sentiment_label: str = "neutral"
    sentiment_confidence: float = 0.5
    aspect_sentiments: List[dict] = Field(default_factory=list)
    topics: List[str] = Field(default_factory=list)
    topic_cluster: Optional[str] = None
    recommendation_tags: List[str] = Field(default_factory=list)
    metadata_json: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

