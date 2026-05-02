"""
SentimentIQ - Topic Routes
"""

from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth import get_current_active_user
from controllers.topic_controller import TopicController
from db.postgres import db_session
from models.user import User
from schemas.topic import Topic, TopicCreate, TopicUpdate, ReviewTopic, ReviewTopicCreate

router = APIRouter(prefix="/topics", tags=["topics"])


@router.get("/", response_model=List[Topic])
async def get_topics(
    session: AsyncSession = Depends(db_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
):
    """Get all topics with pagination"""
    return await TopicController.get_topics(session, skip, limit)


@router.post("/", response_model=Topic, status_code=status.HTTP_201_CREATED)
async def create_topic(
    topic: TopicCreate,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new topic"""
    return await TopicController.create_topic(session, topic, current_user)


@router.get("/{topic_id}", response_model=Topic)
async def get_topic(
    topic_id: int,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Get a topic by ID"""
    return await TopicController.get_topic(session, topic_id)


@router.put("/{topic_id}", response_model=Topic)
async def update_topic(
    topic_id: int,
    topic_update: TopicUpdate,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Update a topic"""
    return await TopicController.update_topic(session, topic_id, topic_update, current_user)


@router.delete("/{topic_id}")
async def delete_topic(
    topic_id: int,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a topic"""
    return await TopicController.delete_topic(session, topic_id, current_user)


@router.post("/review-topics", response_model=ReviewTopic, status_code=status.HTTP_201_CREATED)
async def create_review_topic(
    review_topic: ReviewTopicCreate,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Create a review-topic relationship"""
    return await TopicController.create_review_topic(session, review_topic)


@router.get("/review/{review_id}", response_model=List[Topic])
async def get_topics_for_review(
    review_id: int,
    session: AsyncSession = Depends(db_session),
    current_user: User = Depends(get_current_active_user),
):
    """Get all topics for a specific review"""
    return await TopicController.get_topics_for_review(session, review_id)