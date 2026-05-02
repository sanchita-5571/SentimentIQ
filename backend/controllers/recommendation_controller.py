"""
SentimentIQ - Recommendation Controller
"""

from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.recommendation import RecommendationCreate, RecommendationUpdate, Recommendation
from services.recommendation_service import RecommendationService


class RecommendationController:
    """Controller for recommendation operations"""

    @staticmethod
    async def get_recommendation(session: AsyncSession, recommendation_id: int) -> Recommendation:
        """Get a recommendation by ID"""
        recommendation = await RecommendationService.get_recommendation_by_id(session, recommendation_id)
        if not recommendation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recommendation not found"
            )
        return Recommendation.model_validate(recommendation)

    @staticmethod
    async def get_recommendations(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[Recommendation]:
        """Get all recommendations"""
        recommendations = await RecommendationService.get_recommendations(session, skip, limit)
        return [Recommendation.model_validate(rec) for rec in recommendations]

    @staticmethod
    async def create_recommendation(session: AsyncSession, recommendation_data: RecommendationCreate, current_user: User) -> Recommendation:
        """Create a new recommendation"""
        recommendation = await RecommendationService.create_recommendation(session, recommendation_data)
        return Recommendation.model_validate(recommendation)

    @staticmethod
    async def update_recommendation(session: AsyncSession, recommendation_id: int, recommendation_data: RecommendationUpdate, current_user: User) -> Recommendation:
        """Update an existing recommendation"""
        recommendation = await RecommendationService.update_recommendation(session, recommendation_id, recommendation_data)
        if not recommendation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recommendation not found"
            )
        return Recommendation.model_validate(recommendation)

    @staticmethod
    async def delete_recommendation(session: AsyncSession, recommendation_id: int, current_user: User) -> dict:
        """Delete a recommendation"""
        deleted = await RecommendationService.delete_recommendation(session, recommendation_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recommendation not found"
            )
        return {"message": "Recommendation deleted successfully"}

    @staticmethod
    async def get_recommendations_by_status(session: AsyncSession, status: str, skip: int = 0, limit: int = 100) -> List[Recommendation]:
        """Get recommendations by status"""
        recommendations = await RecommendationService.get_recommendations_by_status(session, status, skip, limit)
        return [Recommendation.model_validate(rec) for rec in recommendations]

    @staticmethod
    async def get_recommendations_by_priority(session: AsyncSession, priority: str, skip: int = 0, limit: int = 100) -> List[Recommendation]:
        """Get recommendations by priority"""
        recommendations = await RecommendationService.get_recommendations_by_priority(session, priority, skip, limit)
        return [Recommendation.model_validate(rec) for rec in recommendations]