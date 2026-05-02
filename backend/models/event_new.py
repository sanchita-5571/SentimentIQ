"""
SentimentIQ - Event Model (Converted to MongoDB)
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Event(BaseModel):
    """MongoDB Event model - external events that may affect sentiment"""
    
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    
    # Event details
    event_type: str  # product_launch, price_change, etc.
    name: str
    description: Optional[str] = None
    
    # Time
    start_date: datetime
    end_date: Optional[datetime] = None
    
    # Impact metrics
    estimated_impact: Optional[float] = None
    actual_impact: Optional[float] = None
    affected_products: Optional[str] = None
    affected_categories: Optional[str] = None
    
    # Source
    source: Optional[str] = None
    external_link: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
