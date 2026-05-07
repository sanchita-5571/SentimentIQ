"""
SentimentIQ - Sentiment Result Model
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SentimentResult(BaseModel):
    """MongoDB Sentiment Result model"""
    
    id: Optional[str] = Field(default=None, alias="_id")
    review_id: str

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

    ml_model_version: Optional[str] = None
    processed_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

    review = relationship("Review", back_populates="sentiment_results")
    
    def __repr__(self):
        return f"<SentimentResult(id={self.id}, review_id={self.review_id}, label={self.final_label})>"
