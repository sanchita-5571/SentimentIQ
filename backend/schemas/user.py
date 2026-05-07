"""
SentimentIQ - User Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    """User update schema"""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6)


class UserResponse(UserBase):
    """User response schema"""
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


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
    source_manual_enabled: bool
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

class Token(BaseModel):
    """Token schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data schema"""
    user_id: Optional[int] = None
    username: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema"""
    refresh_token: str
