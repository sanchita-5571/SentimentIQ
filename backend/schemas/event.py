"""
SentimentIQ - Event Schemas
"""

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

class EventBase(BaseModel):
    """Base event schema"""
    event_type: str
    name: str
    description: Optional[str] = None


class EventCreate(EventBase):
    """Event creation schema"""
    user_id: int
    start_date: datetime
    end_date: Optional[datetime] = None
    estimated_impact: Optional[float] = None
    affected_products: Optional[str] = None
    affected_categories: Optional[str] = None
    external_link: Optional[str] = None


class EventUpdate(BaseModel):
    """Event update schema"""
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    estimated_impact: Optional[float] = None
    actual_impact: Optional[float] = None
    status: Optional[str] = None


class EventResponse(EventBase):
    """Event response schema"""
    id: int
    user_id: int
    start_date: datetime
    end_date: Optional[datetime]
    estimated_impact: Optional[float]
    actual_impact: Optional[float]
    affected_products: Optional[str]
    affected_categories: Optional[str]
    source: Optional[str]
    external_link: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class EventListResponse(BaseModel):
    """Event list response schema"""
    id: int
    event_type: str
    name: str
    start_date: datetime
    end_date: Optional[datetime]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class RootCauseBase(BaseModel):
    """Base root cause schema"""
    cause_type: str
    category: str
    title: str
    description: Optional[str] = None


class RootCauseCreate(RootCauseBase):
    """Root cause creation schema"""
    anomaly_id: int
    event_id: Optional[int] = None
    impact_score: Optional[float] = None
    confidence: Optional[float] = None
    evidence_count: Optional[int] = None
    keywords: Optional[str] = None
    aspects: Optional[str] = None
    recommendation: Optional[str] = None
    priority: Optional[str] = None


class RootCauseUpdate(BaseModel):
    """Root cause update schema"""
    status: Optional[str] = None
    recommendation: Optional[str] = None
    priority: Optional[str] = None


class RootCauseResponse(RootCauseBase):
    """Root cause response schema"""
    id: int
    anomaly_id: int
    event_id: Optional[int]
    impact_score: Optional[float]
    confidence: Optional[float]
    evidence_count: Optional[int]
    keywords: Optional[str]
    aspects: Optional[str]
    recommendation: Optional[str]
    priority: Optional[str]
    status: str
    identified_at: datetime
    confirmed_at: Optional[datetime]
    addressed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class RootCauseListResponse(BaseModel):
    """Root cause list response schema"""
    id: int
    cause_type: str
    category: str
    title: str
    impact_score: Optional[float]
    status: str
    priority: Optional[str]
    identified_at: datetime
    
    class Config:
        from_attributes = True

class EventWithRootCauses(EventResponse):
    """Event with root causes"""
    root_causes: Optional[List[RootCauseListResponse]] = None

class EventStats(BaseModel):
    """Event statistics"""
    total_events: int
    active_events: int
    completed_events: int
    avg_impact: float
    top_events: List[dict]
