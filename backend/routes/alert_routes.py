"""
SentimentIQ - Alert Routes
"""

from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth import get_current_active_user
from controllers.alert_controller import AlertController
from db.postgres import db_session
from models.user import User
from schemas.alert import Alert, AlertCreate, AlertUpdate

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/", response_model=List[Alert])
async def get_alerts(
    session: AsyncSession = Depends(db_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
):
    """Get all alerts with pagination"""
    return await AlertController.get_alerts(session, skip, limit)


@router.post("/", response_model=Alert, status_code=status.HTTP_201_CREATED)
async def create_alert(
    alert: AlertCreate,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new alert"""
    return await AlertController.create_alert(session, alert, current_user)


@router.get("/{alert_id}", response_model=Alert)
async def get_alert(
    alert_id: int,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Get an alert by ID"""
    return await AlertController.get_alert(session, alert_id)


@router.put("/{alert_id}", response_model=Alert)
async def update_alert(
    alert_id: int,
    alert_update: AlertUpdate,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Update an alert"""
    return await AlertController.update_alert(session, alert_id, alert_update, current_user)


@router.delete("/{alert_id}")
async def delete_alert(
    alert_id: int,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Delete an alert"""
    return await AlertController.delete_alert(session, alert_id, current_user)


@router.get("/status/{status}", response_model=List[Alert])
async def get_alerts_by_status(
    status: str,
    session: AsyncSession = Depends(db_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
):
    """Get alerts by status"""
    return await AlertController.get_alerts_by_status(session, status, skip, limit)


@router.get("/type/{alert_type}", response_model=List[Alert])
async def get_alerts_by_type(
    alert_type: str,
    session: AsyncSession = Depends(db_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
):
    """Get alerts by type"""
    return await AlertController.get_alerts_by_type(session, alert_type, skip, limit)


@router.get("/severity/{severity}", response_model=List[Alert])
async def get_alerts_by_severity(
    severity: str,
    session: AsyncSession = Depends(db_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
):
    """Get alerts by severity"""
    return await AlertController.get_alerts_by_severity(session, severity, skip, limit)