"""
MongoDB Database Operations for FastAPI

This module provides MongoDB database operations.
The file name 'postgres.py' is kept for backward compatibility.

NOTE: This file has been refactored from PostgreSQL to MongoDB.
All operations now use MongoDB only.
"""

from db.mongo_ops import (
    USERS_COLLECTION,
    REVIEWS_COLLECTION,
    EVENTS_COLLECTION,
    SETTINGS_COLLECTION,
    INGESTION_BATCHES_COLLECTION,
    BRANDS_COLLECTION,
    ASPECTS_COLLECTION,
    TOPICS_COLLECTION,
    ALERTS_COLLECTION,
    ANOMALIES_COLLECTION,
    RECOMMENDATIONS_COLLECTION,
    get_db_session,
    db_session,
    get_collection,
    find_one,
    find_many,
    insert_one,
    insert_many,
    update_one,
    update_many,
    delete_one,
    delete_many,
    count_documents,
)

__all__ = [
    "USERS_COLLECTION",
    "REVIEWS_COLLECTION",
    "EVENTS_COLLECTION",
    "SETTINGS_COLLECTION",
    "INGESTION_BATCHES_COLLECTION",
    "BRANDS_COLLECTION",
    "ASPECTS_COLLECTION",
    "TOPICS_COLLECTION",
    "ALERTS_COLLECTION",
    "ANOMALIES_COLLECTION",
    "RECOMMENDATIONS_COLLECTION",
    "get_db_session",
    "db_session",
    "get_collection",
    "find_one",
    "find_many",
    "insert_one",
    "insert_many",
    "update_one",
    "update_many",
    "delete_one",
    "delete_many",
    "count_documents",
]
