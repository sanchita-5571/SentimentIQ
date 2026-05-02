"""
SentimentIQ - Review Routes
"""

from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth import get_current_active_user
from controllers.review_controller import ReviewController
from db.postgres import db_session
from models.user import User
from schemas.review import ReviewResponse, ReviewCreate, ReviewUpdate

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/", response_model=List[ReviewResponse])
async def get_reviews(
    session: AsyncSession = Depends(db_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
):
    """Get all reviews with pagination"""
    return await ReviewController.get_reviews(session, skip, limit)


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    review: ReviewCreate,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new review"""
    return await ReviewController.create_review(session, review, current_user)


@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(
    review_id: int,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Get a review by ID"""
    return await ReviewController.get_review(session, review_id)


@router.put("/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Update a review"""
    return await ReviewController.update_review(session, review_id, review_update, current_user)


@router.delete("/{review_id}")
async def delete_review(
    review_id: int,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a review"""
    return await ReviewController.delete_review(session, review_id, current_user)