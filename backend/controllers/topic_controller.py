"""
SentimentIQ - Topic Controller
"""

from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.topic import TopicCreate, TopicUpdate, Topic, ReviewTopicCreate, ReviewTopic
from services.topic_service import TopicService


class TopicController:
    """Controller for topic operations"""

    @staticmethod
    async def get_topic(session: AsyncSession, topic_id: int) -> Topic:
        """Get a topic by ID"""
        topic = await TopicService.get_topic_by_id(session, topic_id)
        if not topic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Topic not found"
            )
        return Topic.model_validate(topic)

    @staticmethod
    async def get_topics(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[Topic]:
        """Get all topics"""
        topics = await TopicService.get_topics(session, skip, limit)
        return [Topic.model_validate(topic) for topic in topics]

    @staticmethod
    async def create_topic(session: AsyncSession, topic_data: TopicCreate, current_user: User) -> Topic:
        """Create a new topic"""
        topic = await TopicService.create_topic(session, topic_data)
        return Topic.model_validate(topic)

    @staticmethod
    async def update_topic(session: AsyncSession, topic_id: int, topic_data: TopicUpdate, current_user: User) -> Topic:
        """Update an existing topic"""
        topic = await TopicService.update_topic(session, topic_id, topic_data)
        if not topic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Topic not found"
            )
        return Topic.model_validate(topic)

    @staticmethod
    async def delete_topic(session: AsyncSession, topic_id: int, current_user: User) -> dict:
        """Delete a topic"""
        deleted = await TopicService.delete_topic(session, topic_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Topic not found"
            )
        return {"message": "Topic deleted successfully"}

    @staticmethod
    async def create_review_topic(session: AsyncSession, review_topic_data: ReviewTopicCreate) -> ReviewTopic:
        """Create a review-topic relationship"""
        review_topic = await TopicService.create_review_topic(session, review_topic_data)
        return ReviewTopic.model_validate(review_topic)

    @staticmethod
    async def get_topics_for_review(session: AsyncSession, review_id: int) -> List[Topic]:
        """Get all topics for a specific review"""
        topics = await TopicService.get_topics_for_review(session, review_id)
        return [Topic.model_validate(topic) for topic in topics]