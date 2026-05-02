"""
SentimentIQ - Brand Routes
"""

from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth import get_current_active_user
from controllers.brand_controller import BrandController
from db.postgres import db_session
from models.user import User
from schemas.brand import Brand, BrandCreate, BrandUpdate

router = APIRouter(prefix="/brands", tags=["brands"])


@router.get("/", response_model=List[Brand])
async def get_brands(
    session: AsyncSession = Depends(db_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
):
    """Get all brands with pagination"""
    return await BrandController.get_brands(session, skip, limit)


@router.post("/", response_model=Brand, status_code=status.HTTP_201_CREATED)
async def create_brand(
    brand: BrandCreate,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new brand"""
    return await BrandController.create_brand(session, brand, current_user)


@router.get("/{brand_id}", response_model=Brand)
async def get_brand(
    brand_id: int,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Get a brand by ID"""
    return await BrandController.get_brand(session, brand_id)


@router.put("/{brand_id}", response_model=Brand)
async def update_brand(
    brand_id: int,
    brand_update: BrandUpdate,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Update a brand"""
    return await BrandController.update_brand(session, brand_id, brand_update, current_user)


@router.delete("/{brand_id}")
async def delete_brand(
    brand_id: int,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a brand"""
    return await BrandController.delete_brand(session, brand_id, current_user)