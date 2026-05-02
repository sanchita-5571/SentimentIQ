"""
SentimentIQ - Sentiment Controller
"""

from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.sentiment import SentimentResultCreate, SentimentResultResponse, SentimentStats
from services.sentiment_service import SentimentService


class SentimentController:
    """Controller for sentiment operations"""

    @staticmethod
    async def get_sentiment_result(session: AsyncSession, sentiment_id: int) -> SentimentResultResponse:
        """Get a sentiment result by ID"""
        sentiment = await SentimentService.get_sentiment_by_id(session, sentiment_id)
        if not sentiment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sentiment result not found"
            )
        return SentimentResultResponse.model_validate(sentiment)

    @staticmethod
    async def get_sentiments_for_review(session: AsyncSession, review_id: int) -> List[SentimentResultResponse]:
        """Get all sentiment results for a review"""
        sentiments = await SentimentService.get_sentiments_for_review(session, review_id)
        return [SentimentResultResponse.model_validate(sentiment) for sentiment in sentiments]

    @staticmethod
    async def create_sentiment_result(session: AsyncSession, sentiment_data: SentimentResultCreate) -> SentimentResultResponse:
        """Create a new sentiment result"""
        sentiment = await SentimentService.create_sentiment_result(session, sentiment_data)
        return SentimentResultResponse.model_validate(sentiment)

    @staticmethod
    async def get_sentiment_stats(session: AsyncSession) -> SentimentStats:
        """Get sentiment statistics"""
        stats = await SentimentService.get_sentiment_stats(session)
        return SentimentStats(**stats)