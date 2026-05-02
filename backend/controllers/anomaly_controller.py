"""
SentimentIQ - Anomaly Controller
"""

from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.anomaly import AnomalyCreate, AnomalyUpdate, AnomalyResponse, AnomalyTriggerCreate, AnomalyTriggerResponse
from services.anomaly_service import AnomalyService


class AnomalyController:
    """Controller for anomaly operations"""

    @staticmethod
    async def get_anomaly(session: AsyncSession, anomaly_id: int) -> AnomalyResponse:
        """Get an anomaly by ID"""
        anomaly = await AnomalyService.get_anomaly_by_id(session, anomaly_id)
        if not anomaly:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Anomaly not found"
            )
        return AnomalyResponse.model_validate(anomaly)

    @staticmethod
    async def get_anomalies(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[AnomalyResponse]:
        """Get all anomalies"""
        anomalies = await AnomalyService.get_anomalies(session, skip, limit)
        return [AnomalyResponse.model_validate(anomaly) for anomaly in anomalies]

    @staticmethod
    async def create_anomaly(session: AsyncSession, anomaly_data: AnomalyCreate, current_user: User) -> AnomalyResponse:
        """Create a new anomaly"""
        anomaly = await AnomalyService.create_anomaly(session, anomaly_data)
        return AnomalyResponse.model_validate(anomaly)

    @staticmethod
    async def update_anomaly(session: AsyncSession, anomaly_id: int, anomaly_data: AnomalyUpdate, current_user: User) -> AnomalyResponse:
        """Update an existing anomaly"""
        anomaly = await AnomalyService.update_anomaly(session, anomaly_id, anomaly_data)
        if not anomaly:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Anomaly not found"
            )
        return AnomalyResponse.model_validate(anomaly)

    @staticmethod
    async def delete_anomaly(session: AsyncSession, anomaly_id: int, current_user: User) -> dict:
        """Delete an anomaly"""
        deleted = await AnomalyService.delete_anomaly(session, anomaly_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Anomaly not found"
            )
        return {"message": "Anomaly deleted successfully"}

    @staticmethod
    async def create_anomaly_trigger(session: AsyncSession, trigger_data: AnomalyTriggerCreate) -> AnomalyTriggerResponse:
        """Create an anomaly trigger"""
        trigger = await AnomalyService.create_anomaly_trigger(session, trigger_data)
        return AnomalyTriggerResponse.model_validate(trigger)