from datetime import datetime

from pydantic import BaseModel, Field


class RootCauseRecommendation(BaseModel):
    title: str
    action: str
    priority: str


class RootCauseEvidence(BaseModel):
    review_id: str
    sentiment_score: float
    snippet: str
    aspects: list[str] = Field(default_factory=list)


class RootCauseEventResponse(BaseModel):
    id: str
    event_date: datetime
    baseline_sentiment: float
    current_sentiment: float
    sentiment_delta: float
    review_volume: int
    earliest_degrading_aspect: str | None = None
    amplification_chain: list[str] = Field(default_factory=list)
    recommendations: list[RootCauseRecommendation] = Field(default_factory=list)
    evidence: list[RootCauseEvidence] = Field(default_factory=list)
    created_at: datetime

    class Config:
        from_attributes = True
