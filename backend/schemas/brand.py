"""
SentimentIQ - Brand Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BrandBase(BaseModel):
    """Base brand schema"""
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    logo_url: Optional[str] = None
    sentiment_threshold: float = 0.05
    anomaly_threshold: float = 0.3
    spam_threshold: float = 0.8


class BrandCreate(BrandBase):
    """Schema for creating a brand"""
    pass


class BrandUpdate(BaseModel):
    """Schema for updating a brand"""
    name: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    logo_url: Optional[str] = None
    sentiment_threshold: Optional[float] = None
    anomaly_threshold: Optional[float] = None
    spam_threshold: Optional[float] = None
    is_active: Optional[bool] = None


class Brand(BrandBase):
    """Full brand schema"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime