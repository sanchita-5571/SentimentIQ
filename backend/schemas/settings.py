"""
SentimentIQ - Settings Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class UserSettingsBase(BaseModel):
    """Base user settings schema"""
    sentiment_threshold_positive: float = 0.05
    sentiment_threshold_negative: float = -0.05
    anomaly_threshold: float = 0.3


class UserSettingsUpdate(UserSettingsBase):
    """User settings update schema"""
    sentiment_threshold_positive: Optional[float] = None
    sentiment_threshold_negative: Optional[float] = None
    anomaly_threshold: Optional[float] = None
    spam_filter_enabled: Optional[bool] = None
    spam_threshold: Optional[float] = None
    language_filter_enabled: Optional[bool] = None
    allowed_languages: Optional[str] = None
    source_csv_enabled: Optional[bool] = None
    source_excel_enabled: Optional[bool] = None
    source_json_enabled: Optional[bool] = None
    source_reddit_enabled: Optional[bool] = None

    email_notifications: Optional[bool] = None
    anomaly_alerts: Optional[bool] = None
    daily_digest: Optional[bool] = None
    dashboard_theme: Optional[str] = None
    sidebarcollapsed: Optional[bool] = None
    items_per_page: Optional[int] = None
    scheduler_enabled: Optional[bool] = None
    analysis_interval_minutes: Optional[int] = None
    anomaly_check_interval_minutes: Optional[int] = None


class UserSettingsResponse(BaseModel):
    """User settings response schema"""
    id: int
    user_id: int
    sentiment_threshold_positive: float
    sentiment_threshold_negative: float
    anomaly_threshold: float
    spam_filter_enabled: bool
    spam_threshold: float
    language_filter_enabled: bool
    allowed_languages: Optional[str]
    source_csv_enabled: bool
    source_excel_enabled: bool
    source_json_enabled: bool
    source_reddit_enabled: bool

    email_notifications: bool
    anomaly_alerts: bool
    daily_digest: bool
    dashboard_theme: str
    sidebarcollapsed: bool
    items_per_page: int
    scheduler_enabled: bool
    analysis_interval_minutes: int
    anomaly_check_interval_minutes: int
    
    class Config:
        from_attributes = True

class SystemSettingsBase(BaseModel):
    """Base system settings schema"""
    key: str
    value: Optional[str] = None
    description: Optional[str] = None


class SystemSettingsCreate(SystemSettingsBase):
    """System settings creation schema"""
    pass


class SystemSettingsUpdate(BaseModel):
    """System settings update schema"""
    value: Optional[str] = None
    description: Optional[str] = None


class SystemSettingsResponse(SystemSettingsBase):
    """System settings response schema"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class DashboardSettings(BaseModel):
    """Dashboard settings schema"""
    theme: str = "light"
    sidebar_collapsed: bool = False
    items_per_page: int = 20
    default_date_range: str = "7d"  # 24h, 7d, 30d, 90d, custom
    chart_type: str = "line"  # line, bar, area

class AlertSettings(BaseModel):
    """Alert settings schema"""
    enabled: bool = True
    email_notifications: bool = True
    anomaly_alerts: bool = True
    daily_digest: bool = False
    alert_channels: list = ["email"]  # email, push, webhook

class AccountSettings(BaseModel):
    """Account settings schema"""
    email: str
    username: str
    full_name: Optional[str] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None


class AccountSettingsResponse(BaseModel):
    """Account settings response schema"""
    email: str
    username: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
