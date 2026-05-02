"""
SentimentIQ - Recommendation Routes
"""

from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth import get_current_active_user
from controllers.recommendation_controller import RecommendationController
from db.postgres import db_session
from models.user import User
from schemas.recommendation import Recommendation, RecommendationCreate, RecommendationUpdate

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/", response_model=List[Recommendation])
async def get_recommendations(
    session: AsyncSession = Depends(db_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
):
    """Get all recommendations with pagination"""
    return await RecommendationController.get_recommendations(session, skip, limit)


@router.post("/", response_model=Recommendation, status_code=status.HTTP_201_CREATED)
async def create_recommendation(
    recommendation: RecommendationCreate,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new recommendation"""
    return await RecommendationController.create_recommendation(session, recommendation, current_user)


@router.get("/{recommendation_id}", response_model=Recommendation)
async def get_recommendation(
    recommendation_id: int,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Get a recommendation by ID"""
    return await RecommendationController.get_recommendation(session, recommendation_id)


@router.put("/{recommendation_id}", response_model=Recommendation)
async def update_recommendation(
    recommendation_id: int,
    recommendation_update: RecommendationUpdate,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Update a recommendation"""
    return await RecommendationController.update_recommendation(session, recommendation_id, recommendation_update, current_user)


@router.delete("/{recommendation_id}")
async def delete_recommendation(
    recommendation_id: int,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a recommendation"""
    return await RecommendationController.delete_recommendation(session, recommendation_id, current_user)


@router.get("/status/{status}", response_model=List[Recommendation])
async def get_recommendations_by_status(
    status: str,
    session: AsyncSession = Depends(db_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
):
    """Get recommendations by status"""
    return await RecommendationController.get_recommendations_by_status(session, status, skip, limit)


@router.get("/priority/{priority}", response_model=List[Recommendation])
async def get_recommendations_by_priority(
    priority: str,
    session: AsyncSession = Depends(db_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
):
    """Get recommendations by priority"""
    return await RecommendationController.get_recommendations_by_priority(session, priority, skip, limit)