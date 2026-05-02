from fastapi import APIRouter, Depends, HTTPException

from api.v1.auth import get_current_user
from db.mongodb import get_mongodb
from schemas.root_cause import RootCauseEventResponse
from services.root_cause_service import get_root_cause_events, rebuild_root_causes

router = APIRouter(prefix="/root-causes", tags=["root-causes"])


@router.get("", response_model=list[RootCauseEventResponse])
async def list_root_causes(
    current_user=Depends(get_current_user),
):
    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")
    return await get_root_cause_events(current_user.id)

@router.post("/rebuild")
async def rebuild_root_cause_events(
    current_user=Depends(get_current_user),
):
    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")
    events = await rebuild_root_causes(current_user.id)
    return {"recomputed": len(events), "events": events}
