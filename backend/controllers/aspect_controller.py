"""
SentimentIQ - Aspect Controller
"""

from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.aspect import AspectCreate, AspectUpdate, Aspect, ReviewAspectCreate, ReviewAspect
from services.aspect_service import AspectService


class AspectController:
    """Controller for aspect operations"""

    @staticmethod
    async def get_aspect(session: AsyncSession, aspect_id: int) -> Aspect:
        """Get an aspect by ID"""
        aspect = await AspectService.get_aspect_by_id(session, aspect_id)
        if not aspect:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aspect not found"
            )
        return Aspect.model_validate(aspect)

    @staticmethod
    async def get_aspects(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[Aspect]:
        """Get all aspects"""
        aspects = await AspectService.get_aspects(session, skip, limit)
        return [Aspect.model_validate(aspect) for aspect in aspects]

    @staticmethod
    async def create_aspect(session: AsyncSession, aspect_data: AspectCreate, current_user: User) -> Aspect:
        """Create a new aspect"""
        aspect = await AspectService.create_aspect(session, aspect_data)
        return Aspect.model_validate(aspect)

    @staticmethod
    async def update_aspect(session: AsyncSession, aspect_id: int, aspect_data: AspectUpdate, current_user: User) -> Aspect:
        """Update an existing aspect"""
        aspect = await AspectService.update_aspect(session, aspect_id, aspect_data)
        if not aspect:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aspect not found"
            )
        return Aspect.model_validate(aspect)

    @staticmethod
    async def delete_aspect(session: AsyncSession, aspect_id: int, current_user: User) -> dict:
        """Delete an aspect"""
        deleted = await AspectService.delete_aspect(session, aspect_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aspect not found"
            )
        return {"message": "Aspect deleted successfully"}

    @staticmethod
    async def create_review_aspect(session: AsyncSession, review_aspect_data: ReviewAspectCreate) -> ReviewAspect:
        """Create a review-aspect relationship"""
        review_aspect = await AspectService.create_review_aspect(session, review_aspect_data)
        return ReviewAspect.model_validate(review_aspect)

    @staticmethod
    async def get_aspects_for_review(session: AsyncSession, review_id: int) -> List[Aspect]:
        """Get all aspects for a specific review"""
        aspects = await AspectService.get_aspects_for_review(session, review_id)
        return [Aspect.model_validate(aspect) for aspect in aspects]