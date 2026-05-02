from datetime import datetime
from typing import Optional

from db.mongodb import get_mongodb
from db.postgres import REVIEWS_COLLECTION
from db.redis_cache import cache_get, cache_set
from db.sql_models import IngestionBatchRecord
from db.sqlite import SessionLocal
from services.nlp_service import aspect_rollup, topic_rollup


def build_filter_query(
    user_id: str,
    search: Optional[str] = None,
    source: Optional[str] = None,
    product: Optional[str] = None,
    category: Optional[str] = None,
    sentiment_label: Optional[str] = None,
    language: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> dict:
    query = {"user_id": user_id}

    if search:
        query["$or"] = [
            {"content": {"$regex": search, "$options": "i"}},
            {"title": {"$regex": search, "$options": "i"}},
            {"topics": {"$regex": search, "$options": "i"}},
            {"aspect_sentiments.aspect": {"$regex": search, "$options": "i"}},
        ]
    if source:
        query["source"] = source
    if product:
        query["product"] = product
    if category:
        query["category"] = category
    if sentiment_label:
        query["sentiment_label"] = sentiment_label
    if language:
        query["language"] = language
    if start_date or end_date:
        query["review_date"] = {}
        if start_date:
            query["review_date"]["$gte"] = start_date
        if end_date:
            query["review_date"]["$lte"] = end_date
    return query


def _aspect_trends(reviews: list[dict]) -> list[dict]:
    if not reviews:
        return []

    ordered = sorted(reviews, key=lambda review: review.get("review_date") or datetime.utcnow())
    split_index = max(len(ordered) // 2, 1)
    baseline_reviews = ordered[:split_index]
    current_reviews = ordered[split_index:]

    baseline_map = {item["aspect"]: item for item in aspect_rollup(baseline_reviews)}
    current_map = {item["aspect"]: item for item in aspect_rollup(current_reviews)}

    combined = []
    for aspect, current in current_map.items():
        previous = baseline_map.get(aspect, {"average_score": 0.0, "mention_count": 0})
        combined.append(
            {
                **current,
                "delta": round(current["average_score"] - previous["average_score"], 4),
            }
        )

    return sorted(combined, key=lambda item: (item["delta"], item["average_score"], -item["mention_count"]))[:8]


async def get_dashboard_snapshot(
    user_id: str,
    filters: dict,
) -> dict:
    cache_key = "dashboard:{user_id}:{source}:{product}:{category}:{sentiment}:{language}:{search}:{start}:{end}".format(
        user_id=user_id,
        source=filters.get("source") or "all",
        product=filters.get("product") or "all",
        category=filters.get("category") or "all",
        sentiment=filters.get("sentiment_label") or "all",
        language=filters.get("language") or "all",
        search=filters.get("search") or "all",
        start=filters.get("start_date") or "all",
        end=filters.get("end_date") or "all",
    )

    cached = await cache_get(cache_key)
    if cached is not None:
        return cached

    db = get_mongodb()
    if db is None:
        raise RuntimeError("MongoDB not connected")

    query = build_filter_query(user_id=user_id, **filters)
    reviews = await db[REVIEWS_COLLECTION].find(query).sort("review_date", 1).to_list(length=10000)

    total_reviews = len(reviews)
    average_sentiment = round(
        sum(review.get("sentiment_score", 0.0) for review in reviews) / total_reviews, 4
    ) if total_reviews else 0.0
    ratings = [review.get("rating") for review in reviews if review.get("rating") is not None]
    average_rating = round(sum(ratings) / len(ratings), 4) if ratings else 0.0
    negative_count = sum(1 for review in reviews if review.get("sentiment_label") == "negative")
    negative_ratio = round(negative_count / total_reviews, 4) if total_reviews else 0.0

    timeline_map: dict[str, dict] = {}
    for review in reviews:
        review_date = review.get("review_date") or datetime.utcnow()
        bucket_date = review_date.replace(hour=0, minute=0, second=0, microsecond=0)
        key = bucket_date.isoformat()
        bucket = timeline_map.setdefault(
            key,
            {
                "date": bucket_date,
                "review_count": 0,
                "negative_reviews": 0,
                "sentiment_total": 0.0,
                "rating_total": 0.0,
                "rating_count": 0,
            },
        )
        bucket["review_count"] += 1
        bucket["sentiment_total"] += review.get("sentiment_score", 0.0)
        if review.get("sentiment_label") == "negative":
            bucket["negative_reviews"] += 1
        if review.get("rating") is not None:
            bucket["rating_total"] += review["rating"]
            bucket["rating_count"] += 1

    timeline = [
        {
            "date": bucket["date"],
            "average_sentiment": round(bucket["sentiment_total"] / bucket["review_count"], 4),
            "average_rating": round(bucket["rating_total"] / bucket["rating_count"], 4) if bucket["rating_count"] else 0.0,
            "review_count": bucket["review_count"],
            "negative_reviews": bucket["negative_reviews"],
        }
        for _, bucket in sorted(timeline_map.items(), key=lambda item: item[0])
    ]

    topics = topic_rollup(reviews)[:8]
    aspect_summary = aspect_rollup(reviews)
    aspect_trends = _aspect_trends(reviews)

    distinct_sources = sorted({review.get("source") for review in reviews if review.get("source")})
    distinct_products = sorted({review.get("product") for review in reviews if review.get("product")})
    distinct_categories = sorted({review.get("category") for review in reviews if review.get("category")})
    distinct_languages = sorted({review.get("language") for review in reviews if review.get("language")})

    with SessionLocal() as session:
        duplicates_removed = (
            session.query(IngestionBatchRecord)
            .filter(IngestionBatchRecord.user_id == user_id)
            .with_entities(IngestionBatchRecord.duplicate_count)
            .all()
        )

    snapshot = {
        "overview": {
            "total_reviews": total_reviews,
            "average_sentiment": average_sentiment,
            "negative_ratio": negative_ratio,
            "average_rating": average_rating,
            "active_topics": len(topics),
            "duplicates_removed": sum(item[0] for item in duplicates_removed),
        },
        "timeline": timeline,
        "aspect_trends": aspect_trends or [
            {
                "aspect": item["aspect"],
                "average_score": item["average_score"],
                "mention_count": item["mention_count"],
                "delta": 0.0,
            }
            for item in aspect_summary[:8]
        ],
        "topics": topics,
        "filter_options": {
            "sources": distinct_sources,
            "products": distinct_products,
            "categories": distinct_categories,
            "languages": distinct_languages,
        },
        "generated_at": datetime.utcnow().isoformat(),
    }

    await cache_set(cache_key, snapshot)
    return snapshot
