"""
SentimentIQ - Aspect Routes
"""

from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth import get_current_active_user
from controllers.aspect_controller import AspectController
from db.postgres import db_session
from models.user import User
from schemas.aspect import Aspect, AspectCreate, AspectUpdate, ReviewAspect, ReviewAspectCreate

router = APIRouter(prefix="/aspects", tags=["aspects"])


@router.get("/", response_model=List[Aspect])
async def get_aspects(
    session: AsyncSession = Depends(db_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
):
    """Get all aspects with pagination"""
    return await AspectController.get_aspects(session, skip, limit)


@router.post("/", response_model=Aspect, status_code=status.HTTP_201_CREATED)
async def create_aspect(
    aspect: AspectCreate,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new aspect"""
    return await AspectController.create_aspect(session, aspect, current_user)


@router.get("/{aspect_id}", response_model=Aspect)
async def get_aspect(
    aspect_id: int,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Get an aspect by ID"""
    return await AspectController.get_aspect(session, aspect_id)


@router.put("/{aspect_id}", response_model=Aspect)
async def update_aspect(
    aspect_id: int,
    aspect_update: AspectUpdate,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Update an aspect"""
    return await AspectController.update_aspect(session, aspect_id, aspect_update, current_user)


@router.delete("/{aspect_id}")
async def delete_aspect(
    aspect_id: int,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Delete an aspect"""
    return await AspectController.delete_aspect(session, aspect_id, current_user)


@router.post("/review-aspects", response_model=ReviewAspect, status_code=status.HTTP_201_CREATED)
async def create_review_aspect(
    review_aspect: ReviewAspectCreate,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Create a review-aspect relationship"""
    return await AspectController.create_review_aspect(session, review_aspect)


@router.get("/review/{review_id}", response_model=List[Aspect])
async def get_aspects_for_review(
    review_id: int,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Get all aspects for a specific review"""
    return await AspectController.get_aspects_for_review(session, review_id)