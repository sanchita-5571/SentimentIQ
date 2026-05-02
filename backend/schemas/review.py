from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class AspectSentiment(BaseModel):
    aspect: str
    score: float
    mentions: int = 1
    keywords: list[str] = Field(default_factory=list)


class ReviewCreate(BaseModel):
    source: str = "manual"
    author: str | None = None
    title: str | None = None
    content: str
    rating: float | None = None
    product: str | None = None
    category: str | None = None
    review_date: datetime | None = None
    external_id: str | None = None
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class ReviewUpdate(BaseModel):
    source: str | None = None
    author: str | None = None
    title: str | None = None
    content: str | None = None
    rating: float | None = None
    product: str | None = None
    category: str | None = None
    review_date: datetime | None = None
    external_id: str | None = None
    metadata_json: dict[str, Any] | None = None


class ReviewResponse(BaseModel):
    id: str
    source: str
    author: str | None = None
    title: str | None = None
    content: str
    language: str
    rating: float | None = None
    product: str | None = None
    category: str | None = None
    sentiment_score: float
    sentiment_label: str
    sentiment_confidence: float
    aspect_sentiments: list[AspectSentiment] = Field(default_factory=list)
    topics: list[str] = Field(default_factory=list)
    topic_cluster: str | None = None
    recommendation_tags: list[str] = Field(default_factory=list)
    is_duplicate: bool
    review_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewListResponse(BaseModel):
    items: list[ReviewResponse]
    total: int
    page: int
    page_size: int


class ManualReviewBatch(BaseModel):
    reviews: list[ReviewCreate]


class IngestionResponse(BaseModel):
    batch_id: str
    created_count: int
    duplicate_count: int
    processed_count: int
    topics_detected: list[str]


class ReviewFilters(BaseModel):
    search: str | None = None
    source: str | None = None
    product: str | None = None
    category: str | None = None
    sentiment_label: str | None = None
    language: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
