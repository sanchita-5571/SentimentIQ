"""
SentimentIQ - Settings API (MongoDB version)
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from api.v1.auth import get_current_active_user
from core.security import hash_password, verify_password
from db.mongodb import get_mongodb
from db.postgres import SETTINGS_COLLECTION

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("/")
async def get_settings(
    current_user=Depends(get_current_active_user),
):
    """Get user settings"""
    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    doc = await db[SETTINGS_COLLECTION].find_one({"user_id": current_user.id, "type": "user"})

    if not doc:
        # Create default settings
        settings_doc = {
            "user_id": current_user.id,
            "type": "user",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        result = await db[SETTINGS_COLLECTION].insert_one(settings_doc)
        settings_doc["_id"] = str(result.inserted_id)
        return settings_doc

    doc["_id"] = str(doc["_id"])
    return doc


@router.put("/")
async def update_settings(
    settings_update: dict,
    current_user=Depends(get_current_active_user),
):
    """Update user settings"""
    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    doc = await db[SETTINGS_COLLECTION].find_one({"user_id": current_user.id, "type": "user"})

    if not doc:
        settings_doc = {
            "user_id": current_user.id,
            "type": "user",
            **settings_update,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        result = await db[SETTINGS_COLLECTION].insert_one(settings_doc)
        settings_doc["_id"] = str(result.inserted_id)
        return settings_doc

    update_data = {k: v for k, v in settings_update.items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()

    await db[SETTINGS_COLLECTION].update_one(
        {"_id": doc["_id"]},
        {"$set": update_data}
    )

    updated_doc = await db[SETTINGS_COLLECTION].find_one({"_id": doc["_id"]})
    updated_doc["_id"] = str(updated_doc["_id"])
    return updated_doc


@router.get("/account")
async def get_account_settings(
    current_user=Depends(get_current_active_user),
):
    """Get account settings"""
    return {
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
    }


@router.put("/account")
async def update_account_settings(
    email: Optional[str] = None,
    full_name: Optional[str] = None,
    current_password: Optional[str] = None,
    new_password: Optional[str] = None,
    current_user=Depends(get_current_active_user),
):
    """Update account settings"""
    if email:
        current_user.email = email
    if full_name is not None:
        current_user.full_name = full_name
    if new_password:
        if not current_password:
            raise HTTPException(status_code=400, detail="Current password is required")
        if current_user.hashed_password and not verify_password(current_password, current_user.hashed_password):
            raise HTTPException(status_code=400, detail="Current password is incorrect")
        current_user.hashed_password = hash_password(new_password)

    return {
        "message": "Account settings updated locally",
        "email": current_user.email,
        "full_name": current_user.full_name,
    }
