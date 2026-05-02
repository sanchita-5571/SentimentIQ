"""
SentimentIQ - Alert Controller
"""

from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.alert import AlertCreate, AlertUpdate, Alert
from services.alert_service import AlertService


class AlertController:
    """Controller for alert operations"""

    @staticmethod
    async def get_alert(session: AsyncSession, alert_id: int) -> Alert:
        """Get an alert by ID"""
        alert = await AlertService.get_alert_by_id(session, alert_id)
        if not alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alert not found"
            )
        return Alert.model_validate(alert)

    @staticmethod
    async def get_alerts(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[Alert]:
        """Get all alerts"""
        alerts = await AlertService.get_alerts(session, skip, limit)
        return [Alert.model_validate(alert) for alert in alerts]

    @staticmethod
    async def create_alert(session: AsyncSession, alert_data: AlertCreate, current_user: User) -> Alert:
        """Create a new alert"""
        alert = await AlertService.create_alert(session, alert_data)
        return Alert.model_validate(alert)

    @staticmethod
    async def update_alert(session: AsyncSession, alert_id: int, alert_data: AlertUpdate, current_user: User) -> Alert:
        """Update an existing alert"""
        alert = await AlertService.update_alert(session, alert_id, alert_data)
        if not alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alert not found"
            )
        return Alert.model_validate(alert)

    @staticmethod
    async def delete_alert(session: AsyncSession, alert_id: int, current_user: User) -> dict:
        """Delete an alert"""
        deleted = await AlertService.delete_alert(session, alert_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alert not found"
            )
        return {"message": "Alert deleted successfully"}

    @staticmethod
    async def get_alerts_by_status(session: AsyncSession, status: str, skip: int = 0, limit: int = 100) -> List[Alert]:
        """Get alerts by status"""
        alerts = await AlertService.get_alerts_by_status(session, status, skip, limit)
        return [Alert.model_validate(alert) for alert in alerts]

    @staticmethod
    async def get_alerts_by_type(session: AsyncSession, alert_type: str, skip: int = 0, limit: int = 100) -> List[Alert]:
        """Get alerts by type"""
        alerts = await AlertService.get_alerts_by_type(session, alert_type, skip, limit)
        return [Alert.model_validate(alert) for alert in alerts]

    @staticmethod
    async def get_alerts_by_severity(session: AsyncSession, severity: str, skip: int = 0, limit: int = 100) -> List[Alert]:
        """Get alerts by severity"""
        alerts = await AlertService.get_alerts_by_severity(session, severity, skip, limit)
        return [Alert.model_validate(alert) for alert in alerts]