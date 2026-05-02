"""
SentimentIQ - Alert Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AlertBase(BaseModel):
    """Base alert schema"""
    title: str
    message: Optional[str] = None
    alert_type: str
    severity: Optional[str] = None
    threshold_value: Optional[float] = None
    actual_value: Optional[float] = None
    source_type: Optional[str] = None
    source_id: Optional[int] = None
    status: str = "active"
    is_email_sent: bool = False
    is_ui_notified: bool = True
    anomaly_id: Optional[int] = None
    root_cause_id: Optional[int] = None


class AlertCreate(AlertBase):
    """Schema for creating an alert"""
    pass


class AlertUpdate(BaseModel):
    """Schema for updating an alert"""
    title: Optional[str] = None
    message: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    acknowledged_by: Optional[int] = None
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[int] = None
    is_email_sent: Optional[bool] = None
    is_ui_notified: Optional[bool] = None


class Alert(AlertBase):
    """Full alert schema"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    acknowledged_at: Optional[datetime] = None
    acknowledged_by: Optional[int] = None
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime