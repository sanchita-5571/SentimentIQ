"""
SentimentIQ - Dashboard API (MongoDB version)
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from api.v1.auth import get_current_user
from db.mongodb import get_mongodb
from schemas.dashboard import DashboardSnapshot
from services.dashboard_service import get_dashboard_snapshot

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/snapshot", response_model=DashboardSnapshot)
async def dashboard_snapshot(
    search: Optional[str] = None,
    source: Optional[str] = None,
    product: Optional[str] = None,
    category: Optional[str] = None,
    sentiment_label: Optional[str] = None,
    language: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user=Depends(get_current_user),
) -> dict:
    """Get dashboard snapshot with filters using MongoDB"""
    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    filters = {
        "search": search,
        "source": source,
        "product": product,
        "category": category,
        "sentiment_label": sentiment_label,
        "language": language,
        "start_date": start_date,
        "end_date": end_date,
    }

    return await get_dashboard_snapshot(current_user.id, filters)
