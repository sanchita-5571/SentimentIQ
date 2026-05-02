"""
SentimentIQ - Events API (MongoDB version)
"""

import json
from datetime import datetime
from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.v1.auth import get_current_active_user
from db.mongodb import get_mongodb
from db.postgres import EVENTS_COLLECTION
from models.event import Event

router = APIRouter()


@router.post("/", response_model=Event, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_data: dict,
    current_user=Depends(get_current_active_user),
):
    """Create a new event"""
    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    event_doc = {
        "user_id": current_user.id,
        "event_type": event_data.get("event_type"),
        "name": event_data.get("name"),
        "description": event_data.get("description"),
        "start_date": event_data.get("start_date"),
        "end_date": event_data.get("end_date"),
        "estimated_impact": event_data.get("estimated_impact"),
        "affected_products": event_data.get("affected_products"),
        "affected_categories": event_data.get("affected_categories"),
        "external_link": event_data.get("external_link"),
        "source": "manual",
        "status": "active",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    result = await db[EVENTS_COLLECTION].insert_one(event_doc)
    event_doc["_id"] = str(result.inserted_id)
    return Event(**event_doc)


@router.get("/", response_model=list[Event])
async def list_events(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    event_type: Optional[str] = None,
    status: Optional[str] = None,
    current_user=Depends(get_current_active_user),
):
    """List all events"""
    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    query = {"user_id": current_user.id}
    if event_type:
        query["event_type"] = event_type
    if status:
        query["status"] = status

    offset = (page - 1) * page_size
    cursor = db[EVENTS_COLLECTION].find(query).sort("start_date", -1).skip(offset).limit(page_size)
    events = await cursor.to_list(length=page_size)

    return [Event(**{**doc, "_id": str(doc["_id"])}) for doc in events]


@router.get("/{event_id}", response_model=Event)
async def get_event(
    event_id: str,
    current_user=Depends(get_current_active_user),
):
    """Get event by ID"""
    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    try:
        doc = await db[EVENTS_COLLECTION].find_one({"_id": ObjectId(event_id), "user_id": current_user.id})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid event ID")

    if not doc:
        raise HTTPException(status_code=404, detail="Event not found")
    return Event(**{**doc, "_id": str(doc["_id"])})


@router.put("/{event_id}", response_model=Event)
async def update_event(
    event_id: str,
    event_update: dict,
    current_user=Depends(get_current_active_user),
):
    """Update an event"""
    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    try:
        doc = await db[EVENTS_COLLECTION].find_one({"_id": ObjectId(event_id), "user_id": current_user.id})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid event ID")

    if not doc:
        raise HTTPException(status_code=404, detail="Event not found")

    update_data = {k: v for k, v in event_update.items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()

    await db[EVENTS_COLLECTION].update_one({"_id": ObjectId(event_id)}, {"$set": update_data})

    updated_doc = await db[EVENTS_COLLECTION].find_one({"_id": ObjectId(event_id)})
    return Event(**{**updated_doc, "_id": str(updated_doc["_id"])})


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: str,
    current_user=Depends(get_current_active_user),
):
    """Delete an event"""
    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    try:
        doc = await db[EVENTS_COLLECTION].find_one({"_id": ObjectId(event_id), "user_id": current_user.id})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid event ID")

    if not doc:
        raise HTTPException(status_code=404, detail="Event not found")

    await db[EVENTS_COLLECTION].delete_one({"_id": ObjectId(event_id)})
    return None
