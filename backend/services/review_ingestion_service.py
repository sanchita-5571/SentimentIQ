"""
SentimentIQ - Review Ingestion Service (MongoDB version)
"""

import io
import json
from datetime import datetime
from uuid import uuid4

import pandas as pd

from db.mongodb import get_mongodb
from db.postgres import REVIEWS_COLLECTION, INGESTION_BATCHES_COLLECTION
from db.sql_models import IngestionBatchRecord
from db.sqlite import SessionLocal
from db.redis_cache import cache_delete_pattern
from services.nlp_service import (
    build_recommendation_tags,
    classify_sentiment,
    clean_text,
    detect_language,
    extract_aspects,
    extract_topics,
    normalized_hash,
)


def parse_csv_bytes(payload: bytes) -> list[dict]:
    """Parse CSV bytes to list of dicts"""
    dataframe = pd.read_csv(io.BytesIO(payload))
    return dataframe.fillna("").to_dict(orient="records")


def parse_json_bytes(payload: bytes) -> list[dict]:
    """Parse JSON bytes to list of dicts"""
    content = json.loads(payload.decode("utf-8"))
    if isinstance(content, dict):
        content = content.get("reviews", [])
    return content


def normalize_review_row(row: dict, source: str) -> dict:
    """Normalize a review row to review data dict"""
    review_date = row.get("review_date")
    if review_date:
        try:
            review_date = pd.to_datetime(review_date).to_pydatetime()
        except Exception:
            review_date = datetime.utcnow()

    return {
        "source": source,
        "author": row.get("author") or row.get("customer") or None,
        "title": row.get("title") or None,
        "content": str(row.get("content") or row.get("review") or row.get("text") or "").strip(),
        "rating": float(row["rating"]) if str(row.get("rating", "")).strip() else None,
        "product": row.get("product") or row.get("product_name") or None,
        "category": row.get("category") or None,
        "review_date": review_date,
        "external_id": str(row.get("id") or row.get("external_id") or "") or None,
        "metadata_json": {"channel": row.get("channel"), "region": row.get("region")},
    }


async def ingest_reviews(
    user_id: str,
    reviews: list[dict],
    source_label: str,
) -> dict:
    """Ingest reviews into MongoDB"""
    batch_id = str(uuid4())
    duplicate_count = 0
    created_reviews = []
    hashes_in_batch = set()
    processed_count = 0

    db = get_mongodb()
    if db is None:
        raise RuntimeError("MongoDB not connected")

    for incoming_review in reviews:
        if not isinstance(incoming_review, dict):
            incoming_review = incoming_review.model_dump()
        processed_count += 1
        cleaned = clean_text(incoming_review.get("content", ""))
        if not cleaned:
            continue

        review_hash = normalized_hash(cleaned)
        if review_hash in hashes_in_batch:
            duplicate_count += 1
            continue

        # Check for duplicates in batch
        existing = await db[REVIEWS_COLLECTION].find_one({"user_id": user_id, "normalized_hash": review_hash})
        if existing:
            duplicate_count += 1
            continue

        hashes_in_batch.add(review_hash)
        language = detect_language(cleaned)
        sentiment_score, sentiment_label, confidence = classify_sentiment(cleaned, language)
        aspects = extract_aspects(cleaned)
        topics = extract_topics([cleaned])[0]

        review_doc = {
            "user_id": user_id,
            "source": source_label,
            "external_id": incoming_review.get("external_id"),
            "author": incoming_review.get("author"),
            "title": incoming_review.get("title"),
            "content": incoming_review.get("content"),
            "cleaned_text": cleaned,
            "language": language,
            "rating": incoming_review.get("rating"),
            "product": incoming_review.get("product"),
            "category": incoming_review.get("category"),
            "review_date": incoming_review.get("review_date") or datetime.utcnow(),
            "normalized_hash": review_hash,
            "sentiment_score": sentiment_score,
            "sentiment_label": sentiment_label,
            "sentiment_confidence": confidence,
            "aspect_sentiments": aspects,
            "recommendation_tags": build_recommendation_tags(aspects, sentiment_label),
            "topics": topics,
            "topic_cluster": topics[0] if topics else "general feedback",
            "metadata_json": incoming_review.get("metadata_json", {}),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        created_reviews.append(review_doc)

    if created_reviews:
        if len(created_reviews) >= 8:
            texts = [review["cleaned_text"] for review in created_reviews]
            all_topics = extract_topics(texts)
            for review, topic_list in zip(created_reviews, all_topics):
                review["topics"] = topic_list
                review["topic_cluster"] = topic_list[0] if topic_list else "general feedback"

        await db[REVIEWS_COLLECTION].insert_many(created_reviews)

    created_at = datetime.utcnow()
    await db[INGESTION_BATCHES_COLLECTION].insert_one(
        {
            "batch_id": batch_id,
            "user_id": user_id,
            "source": source_label,
            "created_at": created_at,
            "created_count": len(created_reviews),
            "duplicate_count": duplicate_count,
            "processed_count": processed_count,
        }
    )

    with SessionLocal() as session:
        session.add(
            IngestionBatchRecord(
                batch_id=batch_id,
                user_id=user_id,
                source=source_label,
                created_count=len(created_reviews),
                duplicate_count=duplicate_count,
                processed_count=processed_count,
                created_at=created_at,
            )
        )
        session.commit()

    # Clear cache
    await cache_delete_pattern(f"dashboard:{user_id}:")
    await cache_delete_pattern(f"root-cause:{user_id}:")

    topics_detected = sorted({topic for review in created_reviews for topic in (review.get("topics") or [])})
    return {
        "batch_id": batch_id,
        "created_count": len(created_reviews),
        "duplicate_count": duplicate_count,
        "processed_count": processed_count,
        "topics_detected": topics_detected,
    }
