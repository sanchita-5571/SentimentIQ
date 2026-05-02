"""
SentimentIQ - Sentiment Schemas
"""

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


# Sentiment Result schemas
class SentimentResultBase(BaseModel):
    """Base sentiment result schema"""
    review_id: int
    vader_positive: Optional[float] = None
    vader_negative: Optional[float] = None
    vader_neutral: Optional[float] = None
    vader_compound: Optional[float] = None
    transformer_label: Optional[str] = None
    transformer_score: Optional[float] = None
    emotion_joy: Optional[float] = None
    emotion_anger: Optional[float] = None
    emotion_sadness: Optional[float] = None
    emotion_fear: Optional[float] = None
    emotion_surprise: Optional[float] = None
    emotion_disgust: Optional[float] = None
    final_score: Optional[float] = None
    final_label: Optional[str] = None
    final_confidence: Optional[float] = None
    aspect_sentiments: Optional[str] = None


class SentimentResultCreate(SentimentResultBase):
    """Sentiment result creation schema"""
    pass


class SentimentResultResponse(SentimentResultBase):
    """Sentiment result response schema"""
    id: int
    ml_model_version: Optional[str]
    processed_at: datetime
    
    class Config:
        from_attributes = True


# Sentiment Analysis schemas
class SentimentAnalysisRequest(BaseModel):
    """Sentiment analysis request schema"""
    text: str
    return_aspects: bool = True
    return_emotions: bool = True
    return_topics: bool = False


class SentimentAnalysisResponse(BaseModel):
    """Sentiment analysis response schema"""
    text: str
    sentiment_score: float
    sentiment_label: str
    sentiment_confidence: float
    aspects: Optional[List[dict]] = None
    emotions: Optional[List[dict]] = None
    topics: Optional[List[str]] = None


# Bulk Sentiment Analysis
class BulkSentimentRequest(BaseModel):
    """Bulk sentiment analysis request"""
    review_ids: List[int]


class BulkSentimentResponse(BaseModel):
    """Bulk sentiment analysis response"""
    processed_count: int
    failed_count: int
    results: List[SentimentAnalysisResponse]


# Sentiment Timeline
class SentimentTimelinePoint(BaseModel):
    """Sentiment timeline point"""
    date: datetime
    avg_sentiment: float
    review_count: int
    positive_count: int
    negative_count: int
    neutral_count: int


class SentimentTimelineRequest(BaseModel):
    """Sentiment timeline request"""
    date_from: datetime
    date_to: datetime
    interval: str = "day"  # hour, day, week, month
    category: Optional[str] = None
    product_name: Optional[str] = None


# Sentiment Statistics
class SentimentStats(BaseModel):
    """Sentiment statistics"""
    total_reviews: int
    avg_sentiment: float
    positive_count: int
    negative_count: int
    neutral_count: int
    positive_percentage: float
    negative_percentage: float
    neutral_percentage: float
    avg_rating: Optional[float]
    anomaly_count: int
