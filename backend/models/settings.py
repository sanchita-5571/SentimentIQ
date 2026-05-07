"""SentimentIQ - Settings Model (MongoDB)"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class UserSettings(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    sentiment_threshold_positive: float = 0.05
    sentiment_threshold_negative: float = -0.05
    anomaly_threshold: float = 0.3
    spam_filter_enabled: bool = True
    spam_threshold: float = 0.8
    language_filter_enabled: bool = False
    allowed_languages: str = "en"
    source_csv_enabled: bool = True
    source_excel_enabled: bool = True
    source_json_enabled: bool = True
    source_reddit_enabled: bool = False
    source_manual_enabled: bool = False
    email_notifications: bool = True
    anomaly_alerts: bool = True
    daily_digest: bool = False
    dashboard_theme: str = "light"
    sidebar_collapsed: bool = False
    items_per_page: int = 20
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    class Config:
        populate_by_name = True

    scheduler_enabled = Column(Boolean, default=True, nullable=False)
    analysis_interval_minutes = Column(Integer, default=60, nullable=False)
    anomaly_check_interval_minutes = Column(Integer, default=30, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="settings")
    
    def __repr__(self):
        return f"<UserSettings(user_id={self.user_id})>"


class SystemSettings(Base):
    """System-wide settings model"""
    
    __tablename__ = "system_settings"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    key = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(Text, nullable=True)
    description = Column(String(500), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<SystemSettings(key={self.key})>"
