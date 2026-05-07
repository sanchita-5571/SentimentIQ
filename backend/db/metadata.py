"""MongoDB Metadata Initialization

Seeds admin/demo users in USERS_COLLECTION if missing.
"""

import asyncio
from datetime import datetime

from core.config import settings
from core.security import hash_password
from db.mongo_ops import USERS_COLLECTION, find_one, insert_one
from models.user import User


async def init_metadata():
    """Initialize metadata collections (users)"""
    seeds = [
        ("admin", settings.ADMIN_EMAIL, "Admin", settings.ADMIN_PASSWORD),
        ("analyst", settings.DEMO_USER_EMAIL, "Demo Analyst", settings.DEMO_USER_PASSWORD),
    ]

    for user_id, email, full_name, password in seeds:
        existing = await find_one(USERS_COLLECTION, {"_id": user_id})
        if not existing:
            user_doc = User(
                id=user_id,
                email=email,
                full_name=full_name,
                hashed_password=hash_password(password),
                is_active=True,
            ).model_dump(by_alias=True)
            await insert_one(USERS_COLLECTION, user_doc)
            print(f"Seeded user: {email}")


async def ensure_demo_user():
    """Get demo analyst user ID, seeding if missing"""
    analyst = await find_one(USERS_COLLECTION, {"email": settings.DEMO_USER_EMAIL})
    if analyst is None:
        await init_metadata()
        analyst = await find_one(USERS_COLLECTION, {"email": settings.DEMO_USER_EMAIL})
        if analyst is None:
            raise RuntimeError("Demo analyst user not created")
    return analyst["id"]
