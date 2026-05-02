"""
SentimentIQ - Sentiment Routes
"""

from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth import get_current_active_user
from controllers.sentiment_controller import SentimentController
from db.postgres import db_session
from models.user import User
from schemas.sentiment import SentimentResultResponse, SentimentResultCreate, SentimentStats

router = APIRouter(prefix="/sentiments", tags=["sentiments"])


@router.get("/stats", response_model=SentimentStats)
async def get_sentiment_stats(
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Get sentiment statistics"""
    return await SentimentController.get_sentiment_stats(session)


@router.post("/results", response_model=SentimentResultResponse, status_code=status.HTTP_201_CREATED)
async def create_sentiment_result(
    sentiment: SentimentResultCreate,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new sentiment result"""
    return await SentimentController.create_sentiment_result(session, sentiment)


@router.get("/results/{sentiment_id}", response_model=SentimentResultResponse)
async def get_sentiment_result(
    sentiment_id: int,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Get a sentiment result by ID"""
    return await SentimentController.get_sentiment_result(session, sentiment_id)


@router.get("/review/{review_id}", response_model=List[SentimentResultResponse])
async def get_sentiments_for_review(
    review_id: int,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Get all sentiment results for a review"""
    return await SentimentController.get_sentiments_for_review(session, review_id)