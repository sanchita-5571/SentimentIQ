"""
SentimentIQ - Anomaly Schemas
"""

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


# Anomaly schemas
class AnomalyBase(BaseModel):
    """Base anomaly schema"""
    anomaly_type: str
    severity: str
    title: str
    description: Optional[str] = None


class AnomalyCreate(AnomalyBase):
    """Anomaly creation schema"""
    user_id: int
    baseline_score: Optional[float] = None
    current_score: Optional[float] = None
    deviation: Optional[float] = None
    deviation_percentage: Optional[float] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    affected_reviews: Optional[int] = None
    affected_products: Optional[str] = None
    affected_categories: Optional[str] = None


class AnomalyUpdate(BaseModel):
    """Anomaly update schema"""
    status: Optional[str] = None
    resolution_notes: Optional[str] = None
    end_date: Optional[datetime] = None


class AnomalyResponse(AnomalyBase):
    """Anomaly response schema"""
    id: int
    user_id: int
    baseline_score: Optional[float]
    current_score: Optional[float]
    deviation: Optional[float]
    deviation_percentage: Optional[float]
    start_date: datetime
    end_date: Optional[datetime]
    duration_minutes: Optional[int]
    affected_reviews: Optional[int]
    affected_products: Optional[str]
    affected_categories: Optional[str]
    status: str
    resolved_at: Optional[datetime]
    resolution_notes: Optional[str]
    detected_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AnomalyListResponse(BaseModel):
    """Anomaly list response schema"""
    id: int
    anomaly_type: str
    severity: str
    title: str
    start_date: datetime
    status: str
    detected_at: datetime
    
    class Config:
        from_attributes = True


# Anomaly Trigger schemas
class AnomalyTriggerBase(BaseModel):
    """Base anomaly trigger schema"""
    anomaly_id: int
    review_id: int
    trigger_type: str


class AnomalyTriggerCreate(AnomalyTriggerBase):
    """Anomaly trigger creation schema"""
    contribution_score: Optional[float] = None


class AnomalyTriggerResponse(AnomalyTriggerBase):
    """Anomaly trigger response schema"""
    id: int
    contribution_score: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Anomaly Statistics
class AnomalyStats(BaseModel):
    """Anomaly statistics"""
    total_anomalies: int
    active_anomalies: int
    resolved_anomalies: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    avg_resolution_time_hours: Optional[float]
    top_issues: List[dict]


# Anomaly Filter
class AnomalyFilter(BaseModel):
    """Anomaly filter schema"""
    anomaly_type: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
