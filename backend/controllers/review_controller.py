"""
SentimentIQ - Review Controller
"""

from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse
from services.review_service import ReviewService


class ReviewController:
    """Controller for review operations"""

    @staticmethod
    async def get_review(session: AsyncSession, review_id: int) -> ReviewResponse:
        """Get a review by ID"""
        review = await ReviewService.get_review_by_id(session, review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found"
            )
        return ReviewResponse.model_validate(review)

    @staticmethod
    async def get_reviews(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[ReviewResponse]:
        """Get all reviews"""
        reviews = await ReviewService.get_reviews(session, skip, limit)
        return [ReviewResponse.model_validate(review) for review in reviews]

    @staticmethod
    async def create_review(session: AsyncSession, review_data: ReviewCreate, current_user: User) -> ReviewResponse:
        """Create a new review"""
        review = await ReviewService.create_review(session, review_data)
        return ReviewResponse.model_validate(review)

    @staticmethod
    async def update_review(session: AsyncSession, review_id: int, review_data: ReviewUpdate, current_user: User) -> ReviewResponse:
        """Update an existing review"""
        review = await ReviewService.update_review(session, review_id, review_data)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found"
            )
        return ReviewResponse.model_validate(review)

    @staticmethod
    async def delete_review(session: AsyncSession, review_id: int, current_user: User) -> dict:
        """Delete a review"""
        deleted = await ReviewService.delete_review(session, review_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found"
            )
        return {"message": "Review deleted successfully"}