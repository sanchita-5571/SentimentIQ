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
from db.redis_cache import cache_delete_pattern
from services.nlp_service import (
    build_recommendation_tags,
    classify_sentiment,
    clean_text,
    detect_language,
    extract_aspects,
    extract_topics,
    get_vader,
    normalized_hash_from_cleaned,
)


def _parse_rating(value) -> float | None:
    try:
        return float(value) if value not in ("", None) else None
    except (TypeError, ValueError):
        return None


async def parse_csv_bytes(payload: bytes) -> list[dict]:
    """Parse CSV bytes to list of dicts (async)"""
    def _parse():
        read_kwargs = {
            "skipinitialspace": True,
            "low_memory": False,
        }
        for encoding in ("utf-8", "utf-8-sig", "latin1"):
            try:
                dataframe = pd.read_csv(io.BytesIO(payload), encoding=encoding, **read_kwargs)
                break
            except UnicodeDecodeError:
                continue
            except Exception:
                if encoding == "latin1":
                    raise
        else:
            dataframe = pd.read_csv(io.BytesIO(payload), encoding="latin1", **read_kwargs)

        dataframe.columns = [str(column).strip().lower() for column in dataframe.columns]
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
    normalized_row = {str(key).strip().lower(): value for key, value in row.items()}


    content_keys = ['content', 'review', 'text', 'comment', 'feedback', 'description', 'message', 'body']
    content = ''
    for key in content_keys:
        if key in normalized_row and normalized_row[key]:
            content = str(normalized_row[key]).strip()
            break

    summary = str(normalized_row.get("summary") or "").strip()
    if summary and content and summary not in content:
        content = f"{summary}. {content}"
    elif summary and not content:
        content = summary
    
    if not content:

        all_text = ' '.join([str(v) for v in normalized_row.values() if isinstance(v, str) and len(str(v)) > 5])
        content = all_text[:1000]
    
    review_date = normalized_row.get("review_date") or normalized_row.get("time") or normalized_row.get("date")
    if review_date:
        try:
            if isinstance(review_date, (int, float)) or (isinstance(review_date, str) and str(review_date).isdigit()):
                review_date = pd.to_datetime(int(float(review_date)), unit="s", utc=True).to_pydatetime()
            else:
                review_date = pd.to_datetime(review_date).to_pydatetime()
        except Exception:
            review_date = datetime.utcnow()
    else:
        review_date = datetime.utcnow()

    external_id = normalized_row.get("id") or normalized_row.get("external_id") or normalized_row.get("row")
    external_id = str(external_id) if external_id not in ("", None) else None

    return {
        "source": source,
        "author": normalized_row.get("author") or normalized_row.get("customer") or normalized_row.get("profilename") or None,
        "title": normalized_row.get("title") or normalized_row.get("subject") or summary or None,
        "content": content or "",
        "rating": _parse_rating(normalized_row.get("rating") or normalized_row.get("score")),
        "product": normalized_row.get("product") or normalized_row.get("product_name") or normalized_row.get("item") or normalized_row.get("productid") or None,
        "category": normalized_row.get("category") or None,
        "review_date": review_date,
        "external_id": external_id,
        "metadata_json": {
            k: v
            for k, v in normalized_row.items()
            if k not in ['content', 'review', 'text', 'summary', 'rating', 'score', 'product', 'product_name', 'productid']
        },
    }


@timer
async def ingest_reviews(
    user_id: str,
    reviews: list[dict],
    source_label: str,
    batch_metadata: dict | None = None,
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
        review_hash = normalized_hash_from_cleaned(cleaned)
        if review_hash in hashes_in_batch:
            duplicate_count += 1
            continue
        hashes_in_batch.add(review_hash)
        candidate_data.append((incoming_review, cleaned))
        hashes_list.append(review_hash)
    print(f"[TIMING] Preprocessing loop took {time.perf_counter() - start_loop:.2f}s for {len(candidate_data)} candidates")

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
                "batch_id": batch_id,
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
    batch_record = {
        "batch_id": batch_id,
        "user_id": user_id,
        "source": source_label,
        "created_at": created_at,
        "created_count": len(created_reviews),
        "duplicate_count": duplicate_count,
        "processed_count": processed_count,
        "file_name": batch_metadata.get("file_name") if batch_metadata else None,
        "metadata_json": batch_metadata.get("metadata_json") if batch_metadata else {},
    }
    await db[INGESTION_BATCHES_COLLECTION].insert_one(batch_record)

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
