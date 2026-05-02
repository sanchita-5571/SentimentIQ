"""
SentimentIQ - Alert Model
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Alert(BaseModel):
    """MongoDB Alert model for notifications and triggers"""

    id: Optional[str] = Field(default=None, alias="_id")
    title: str
    message: Optional[str] = None
    alert_type: str  # anomaly, sentiment_drop, volume_spike

    # Alert configuration
    severity: Optional[str] = None  # critical, high, medium, low
    threshold_value: Optional[float] = None  # The threshold that was exceeded
    actual_value: Optional[float] = None  # The actual value that triggered the alert

    # Source information
    source_type: Optional[str] = None  # review, sentiment, anomaly
    source_id: Optional[str] = None  # ID of the source record

    # Status
    status: str = "active"  # active, acknowledged, resolved
    acknowledged_at: Optional[datetime] = None
    acknowledged_by: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None

    # Notification settings
    is_email_sent: bool = False
    is_ui_notified: bool = True

    # Relationships
    anomaly_id: Optional[str] = None
    root_cause_id: Optional[str] = None

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

    # Relationships
    acknowledged_user = relationship("User", foreign_keys=[acknowledged_by], lazy="selectin")
    resolved_user = relationship("User", foreign_keys=[resolved_by], lazy="selectin")
    anomaly = relationship("Anomaly", back_populates="alerts", lazy="selectin")
    root_cause = relationship("RootCause", back_populates="alerts", lazy="selectin")

    def __repr__(self):
        return f"<Alert(id={self.id}, title={self.title}, severity={self.severity}, status={self.status})>"