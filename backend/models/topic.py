"""SentimentIQ - Topic Model (MongoDB)"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Topic(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
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
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    class Config:
        populate_by_name = True

class ReviewTopic(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    review_id: str
    topic_id: str
    probability: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    class Config:
        populate_by_name = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    review_id = Column(Integer, ForeignKey("reviews.id"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False, index=True)
    probability = Column(Float, nullable=True)  # Probability of this topic for this review

    review = relationship("Review", back_populates="review_topics", lazy="selectin")
    topic = relationship("Topic", back_populates="reviews", lazy="selectin")

    def __repr__(self):
        return f"<ReviewTopic(review_id={self.review_id}, topic_id={self.topic_id})>"