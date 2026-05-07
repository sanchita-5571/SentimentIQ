"""SentimentIQ - Dashboard Snapshot History API (MongoDB version)"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from api.v1.auth import get_current_user
from services.dashboard_history_service import (
    list_dashboard_snapshot_history,
    store_dashboard_snapshot_history,
)
from schemas.dashboard_history import (
    DashboardHistoryCreateRequest,
    DashboardHistoryEntry,
)

router = APIRouter(prefix="/dashboard/history", tags=["dashboard-history"])


@router.post("/store", response_model=dict)
async def store_dashboard_history(
    payload: DashboardHistoryCreateRequest,
    current_user=Depends(get_current_user),
) -> dict:
    try:
        return await store_dashboard_snapshot_history(
            current_user.id,
            batch_id=payload.batch_id,
            filters=payload.filters,
            snapshot=payload.snapshot.model_dump(),
            root_causes=payload.root_causes,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list", response_model=list[DashboardHistoryEntry])
async def list_dashboard_history(
    search: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    current_user=Depends(get_current_user),
):
    try:
        return await list_dashboard_snapshot_history(
            current_user.id,
            search=search,
            limit=limit,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

