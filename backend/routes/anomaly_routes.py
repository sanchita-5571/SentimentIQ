"""
SentimentIQ - Anomaly Routes
"""

from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth import get_current_active_user
from controllers.anomaly_controller import AnomalyController
from db.postgres import db_session
from models.user import User
from schemas.anomaly import AnomalyResponse, AnomalyCreate, AnomalyUpdate, AnomalyTriggerResponse, AnomalyTriggerCreate

router = APIRouter(prefix="/anomalies", tags=["anomalies"])


@router.get("/", response_model=List[AnomalyResponse])
async def get_anomalies(
    session: AsyncSession = Depends(db_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
):
    """Get all anomalies with pagination"""
    return await AnomalyController.get_anomalies(session, skip, limit)


@router.post("/", response_model=AnomalyResponse, status_code=status.HTTP_201_CREATED)
async def create_anomaly(
    anomaly: AnomalyCreate,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new anomaly"""
    return await AnomalyController.create_anomaly(session, anomaly, current_user)


@router.get("/{anomaly_id}", response_model=AnomalyResponse)
async def get_anomaly(
    anomaly_id: int,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Get an anomaly by ID"""
    return await AnomalyController.get_anomaly(session, anomaly_id)


@router.put("/{anomaly_id}", response_model=AnomalyResponse)
async def update_anomaly(
    anomaly_id: int,
    anomaly_update: AnomalyUpdate,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Update an anomaly"""
    return await AnomalyController.update_anomaly(session, anomaly_id, anomaly_update, current_user)


@router.delete("/{anomaly_id}")
async def delete_anomaly(
    anomaly_id: int,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Delete an anomaly"""
    return await AnomalyController.delete_anomaly(session, anomaly_id, current_user)


@router.post("/triggers", response_model=AnomalyTriggerResponse, status_code=status.HTTP_201_CREATED)
async def create_anomaly_trigger(
    trigger: AnomalyTriggerCreate,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Create an anomaly trigger"""
    return await AnomalyController.create_anomaly_trigger(session, trigger)