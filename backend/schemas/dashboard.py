from datetime import datetime

from pydantic import BaseModel, Field


class OverviewMetrics(BaseModel):
    total_reviews: int
    average_sentiment: float
    negative_ratio: float
    average_rating: float
    active_topics: int
    duplicates_removed: int


class TimelinePoint(BaseModel):
    date: datetime
    average_sentiment: float
    average_rating: float
    review_count: int
    negative_reviews: int


class AspectTrend(BaseModel):
    aspect: str
    average_score: float
    mention_count: int
    delta: float


class TopicSummary(BaseModel):
    topic: str
    mentions: int
    avg_sentiment: float


class FilterOptions(BaseModel):
    sources: list[str] = Field(default_factory=list)
    products: list[str] = Field(default_factory=list)
    categories: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)


class DashboardSnapshot(BaseModel):
    overview: OverviewMetrics
    timeline: list[TimelinePoint]
    aspect_trends: list[AspectTrend]
    topics: list[TopicSummary]
    filter_options: FilterOptions
    generated_at: datetime
