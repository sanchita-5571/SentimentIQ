from datetime import datetime
from typing import Any, Optional

from db.mongodb import get_mongodb
from db.postgres import REVIEWS_COLLECTION, INGESTION_BATCHES_COLLECTION
from db.redis_cache import cache_delete_pattern
from services.nlp_service import (
    build_recommendation_tags,
    classify_sentiment,
    clean_text,
    detect_language,
    extract_aspects,
    extract_topics,
    get_vader,
)


def _normalize_reviews_for_rerun(reviews: list[dict]) -> list[dict]:
    if not reviews:
        return []

    cleaned_texts = [clean_text(review.get("content", "")) for review in reviews]
    languages = [detect_language(text) for text in cleaned_texts]
    vader_scores = [get_vader().polarity_scores(text)["compound"] for text in cleaned_texts]
    sentiments = [
        classify_sentiment(text, lang, vader_score=score)
        for text, lang, score in zip(cleaned_texts, languages, vader_scores)
    ]
    aspects_list = [
        extract_aspects(text, polarity_score=score)
        for text, score in zip(cleaned_texts, vader_scores)
    ]
    all_topics = extract_topics(cleaned_texts)

    updates = []
    for i, review in enumerate(reviews):
        sentiment_score, sentiment_label, sentiment_confidence = sentiments[i]
        aspect_sentiments = aspects_list[i]
        updates.append(
            {
                "_id": review.get("_id"),
                "sentiment_score": sentiment_score,
                "sentiment_label": sentiment_label,
                "sentiment_confidence": sentiment_confidence,
                "aspect_sentiments": aspect_sentiments,
                "recommendation_tags": build_recommendation_tags(aspect_sentiments, sentiment_label),
                "topics": all_topics[i],
                "topic_cluster": all_topics[i][0] if all_topics[i] else "general feedback",
                "updated_at": datetime.utcnow(),
            }
        )
    return updates


async def list_review_batches(user_id: str, search: Optional[str] = None) -> list[dict]:
    db = get_mongodb()
    if db is None:
        return []

    query = {"user_id": user_id}
    if search:
        query["$or"] = [
            {"file_name": {"$regex": search, "$options": "i"}},
            {"source": {"$regex": search, "$options": "i"}},
        ]

    cursor = db[INGESTION_BATCHES_COLLECTION].find(query).sort("created_at", -1)
    return await cursor.to_list(length=100)


async def get_review_batch(user_id: str, batch_id: str) -> dict | None:
    db = get_mongodb()
    if db is None:
        return None

    return await db[INGESTION_BATCHES_COLLECTION].find_one({"user_id": user_id, "batch_id": batch_id})


async def update_review_batch_metadata(user_id: str, batch_id: str, file_name: str | None = None, metadata_json: dict[str, Any] | None = None) -> dict | None:
    db = get_mongodb()
    if db is None:
        return None

    update_fields: dict[str, Any] = {}
    if file_name is not None:
        update_fields["file_name"] = file_name
    if metadata_json is not None:
        update_fields["metadata_json"] = metadata_json
    if not update_fields:
        return await get_review_batch(user_id, batch_id)

    await db[INGESTION_BATCHES_COLLECTION].update_one(
        {"user_id": user_id, "batch_id": batch_id},
        {"$set": update_fields},
    )
    return await get_review_batch(user_id, batch_id)


async def delete_review_batch(user_id: str, batch_id: str) -> dict:
    db = get_mongodb()
    if db is None:
        return {"deleted_reviews": 0, "deleted_batch": 0}

    review_query = {"user_id": user_id, "batch_id": batch_id}
    deleted_reviews = await db[REVIEWS_COLLECTION].delete_many(review_query)
    deleted_batch = await db[INGESTION_BATCHES_COLLECTION].delete_one({"user_id": user_id, "batch_id": batch_id})
    await cache_delete_pattern(f"dashboard:{user_id}:")
    await cache_delete_pattern(f"root-cause:{user_id}:")
    return {
        "deleted_reviews": deleted_reviews.deleted_count if hasattr(deleted_reviews, "deleted_count") else 0,
        "deleted_batch": deleted_batch.deleted_count if hasattr(deleted_batch, "deleted_count") else 0,
    }


async def rerun_review_batch(user_id: str, batch_id: str) -> dict:
    db = get_mongodb()
    if db is None:
        raise RuntimeError("MongoDB not connected")

    query = {"user_id": user_id, "batch_id": batch_id}
    reviews = await db[REVIEWS_COLLECTION].find(query).to_list(length=10000)
    updates = _normalize_reviews_for_rerun(reviews)
    reprocessed_count = 0
    for update in updates:
        review_id = update.pop("_id")
        await db[REVIEWS_COLLECTION].update_one({"_id": review_id, "user_id": user_id}, {"$set": update})
        reprocessed_count += 1

    await cache_delete_pattern(f"dashboard:{user_id}:")
    await cache_delete_pattern(f"root-cause:{user_id}:")
    return {
        "batch_id": batch_id,
        "created_count": len(reviews),
        "duplicate_count": 0,
        "processed_count": reprocessed_count,
        "message": "Batch rerun completed",
    }
