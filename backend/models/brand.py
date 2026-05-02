"""
SentimentIQ - Brand Model
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Brand(BaseModel):
    """MongoDB Brand model"""

    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    logo_url: Optional[str] = None

    # Settings
    sentiment_threshold: float = 0.05
    anomaly_threshold: float = 0.3
    spam_threshold: float = 0.8

    # Metadata
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True


class BrandSettings(BaseModel):
    """MongoDB Brand Settings model"""

    id: Optional[str] = Field(default=None, alias="_id")
    brand_id: str
    settings: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True