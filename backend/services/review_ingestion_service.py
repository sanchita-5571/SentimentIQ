"""
SentimentIQ - Review Ingestion Service (MongoDB version) - PERFORMANCE TIMING
"""

import asyncio
import io
import json
import time
from datetime import datetime
from uuid import uuid4
from functools import wraps

import pandas as pd
import re

def timer(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[TIMING] {func.__name__} took {end - start:.2f}s")
        return result
    return wrapper

def timer_sync(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[TIMING] {func.__name__} took {end - start:.2f}s")
        return result
    return wrapper

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
    get_vader,
    normalized_hash,
)


def _parse_rating(value) -> float | None:
    try:
        return float(value) if value not in ("", None) else None
    except (TypeError, ValueError):
        return None


async def parse_csv_bytes(payload: bytes) -> list[dict]:
    """Parse CSV bytes to list of dicts (async)"""
    def _parse():
        try:
            dataframe = pd.read_csv(io.BytesIO(payload), encoding="utf-8", engine="python", skipinitialspace=True)
        except UnicodeDecodeError:
            dataframe = pd.read_csv(io.BytesIO(payload), encoding="utf-8-sig", engine="python", skipinitialspace=True)
        except Exception:
            dataframe = pd.read_csv(io.BytesIO(payload), encoding="latin1", engine="python", skipinitialspace=True)
        return dataframe.fillna("").to_dict(orient="records")
    return await asyncio.to_thread(_parse)


def parse_json_bytes(payload: bytes) -> list[dict]:
    """Parse JSON bytes to list of dicts"""
    content = json.loads(payload.decode("utf-8"))
    if isinstance(content, dict):
        content = content.get("reviews", [])
    return content


def normalize_review_row(row: dict, source: str) -> dict:
    """Normalize a review row to review data dict - flexible text extraction"""
    # Support flexible upload schemas without dropping decimals, dates, or optional ids from user files.
    # Check multiple possible column names for content
    content_keys = ['content', 'review', 'text', 'comment', 'feedback', 'description', 'message', 'body', 'summary']
    content = ''
    for key in content_keys:
        if key in row and row[key]:
            content = str(row[key]).strip()
            break
    
    if not content:
        # Fallback: join all string values longer than 5 chars
        all_text = ' '.join([str(v) for v in row.values() if isinstance(v, str) and len(str(v)) > 5])
        content = all_text[:1000]
    
    review_date = row.get("review_date")
    if review_date:
        try:
            review_date = pd.to_datetime(review_date).to_pydatetime()
        except Exception:
            review_date = datetime.utcnow()
    else:
        review_date = datetime.utcnow()

    external_id = row.get("id") or row.get("external_id") or row.get("row")
    external_id = str(external_id) if external_id not in ("", None) else None

    return {
        "source": source,
        "author": row.get("author") or row.get("customer") or None,
        "title": row.get("title") or row.get("subject") or None,
        "content": content or "",
        "rating": _parse_rating(row.get("rating")),
        "product": row.get("product") or row.get("product_name") or row.get("item") or None,
        "category": row.get("category") or None,
        "review_date": review_date,
        "external_id": external_id,
        "metadata_json": {k: v for k, v in row.items() if k not in ['content', 'review', 'text', 'rating', 'product']},
    }


@timer
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

    start_loop = time.perf_counter()
    candidate_data = []
    hashes_list = []
    for incoming_review in reviews:
        if not isinstance(incoming_review, dict):
            incoming_review = incoming_review.model_dump()
        processed_count += 1
        raw_content = incoming_review.get("content", "")
        cleaned = clean_text(raw_content)
        if not cleaned:
            continue
        review_hash = normalized_hash(cleaned)
        if review_hash in hashes_in_batch:
            duplicate_count += 1
            continue
        hashes_in_batch.add(review_hash)
        candidate_data.append((incoming_review, cleaned))
        hashes_list.append(review_hash)
    print(f"[TIMING] Preprocessing loop took {time.perf_counter() - start_loop:.2f}s for {len(candidate_data)} candidates")

    # Bulk duplicate check + filter
    if candidate_data:
        existing_hashes = await db[REVIEWS_COLLECTION].distinct("normalized_hash", {"user_id": user_id, "normalized_hash": {"$in": hashes_list}})
        existing_set = set(existing_hashes)
        filtered_data = []
        filtered_hashes = []
        for i, h in enumerate(hashes_list):
            if h not in existing_set:
                filtered_data.append(candidate_data[i])
                filtered_hashes.append(h)
            else:
                duplicate_count += 1
        print(f"[TIMING] Bulk dedupe complete. {duplicate_count} duplicates, {len(filtered_data)} new reviews to process")

        # Batch NLP
        batch_start = time.perf_counter()
        cleaned_texts = [data[1] for data in filtered_data]
        languages = [detect_language(text) for text in cleaned_texts]
        vader_scores = [score["compound"] for score in [get_vader().polarity_scores(text) for text in cleaned_texts]]
        sentiments = [
            classify_sentiment(text, lang, vader_score=score)
            for text, lang, score in zip(cleaned_texts, languages, vader_scores)
        ]
        aspects_list = [
            extract_aspects(text, polarity_score=score)
            for text, score in zip(cleaned_texts, vader_scores)
        ]
        all_topics = extract_topics(cleaned_texts)
        print(f"[TIMING] Batch NLP took {time.perf_counter() - batch_start:.2f}s")

        for i, (incoming_review, cleaned) in enumerate(filtered_data):
            review_doc = {
                "user_id": user_id,
                "source": source_label,
                "external_id": incoming_review.get("external_id"),
                "author": incoming_review.get("author"),
                "title": incoming_review.get("title"),
                "content": incoming_review.get("content"),
                "cleaned_text": cleaned,
                "language": languages[i],
                "rating": incoming_review.get("rating"),
                "product": incoming_review.get("product"),
                "category": incoming_review.get("category"),
                "review_date": incoming_review.get("review_date") or datetime.utcnow(),
                "normalized_hash": filtered_hashes[i],
                "sentiment_score": sentiments[i][0],
                "sentiment_label": sentiments[i][1],
                "sentiment_confidence": sentiments[i][2],
                "aspect_sentiments": aspects_list[i],
                "recommendation_tags": build_recommendation_tags(aspects_list[i], sentiments[i][1]),
                "topics": all_topics[i],
                "topic_cluster": all_topics[i][0] if all_topics[i] else "general feedback",
                "metadata_json": incoming_review.get("metadata_json", {}),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
            created_reviews.append(review_doc)

    if created_reviews:
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
