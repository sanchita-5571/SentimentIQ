"""
SentimentIQ - Root Cause Service (MongoDB version)
"""

from datetime import datetime
from typing import List, Optional

from core.config import settings
from db.mongodb import get_mongodb
from db.postgres import EVENTS_COLLECTION, REVIEWS_COLLECTION
from db.redis_cache import cache_delete_pattern, cache_get, cache_set
from services.nlp_service import aspect_rollup


def _recommendations_for_aspect(aspect: Optional[str]) -> List[dict]:
    """Get recommendations for a specific aspect"""
    aspect = aspect or "general"
    playbooks = {
        "shipping": [
            {
                "title": "Stabilize courier SLA",
                "action": "Audit late-delivery lanes and switch the lowest-performing partner within 72 hours.",
                "priority": "high",
            },
            {
                "title": "Proactive shipping comms",
                "action": "Send delay notifications with revised ETA and compensation credit before support tickets spike.",
                "priority": "medium",
            },
        ],
        "quality": [
            {
                "title": "Quarantine defect-prone batches",
                "action": "Trace affected SKUs by manufacturing batch and hold inventory until QA passes.",
                "priority": "high",
            }
        ],
        "support": [
            {
                "title": "Shorten first-response time",
                "action": "Create a negative-review queue and staff live agents during peak complaint windows.",
                "priority": "high",
            }
        ],
    }
    return playbooks.get(
        aspect,
        [
            {
                "title": "Launch focused remediation sprint",
                "action": "Review the linked verbatims, align owners, and ship the highest-frequency fix this week.",
                "priority": "medium",
            }
        ],
    )


async def rebuild_root_causes(user_id: str) -> List[dict]:
    """Rebuild root cause events for a user"""
    db = get_mongodb()
    if db is None:
        return []

    # Get all reviews for user
    cursor = db[REVIEWS_COLLECTION].find({"user_id": user_id}).sort("review_date", 1)
    reviews = await cursor.to_list(length=10000)

    if len(reviews) < 6:
        return []

    # Delete existing root cause events
    await db[EVENTS_COLLECTION].delete_many({"user_id": user_id, "type": "root_cause"})

    # Group reviews by day
    daily = {}
    for review in reviews:
        review_date = review.get("review_date")
        if review_date:
            day = review_date.replace(hour=0, minute=0, second=0, microsecond=0)
            daily.setdefault(day, []).append(review)

    ordered_days = sorted(daily.keys())
    events = []

    for idx, day in enumerate(ordered_days[3:], start=3):
        baseline_days = ordered_days[max(0, idx - 3):idx]
        baseline_reviews = [review for bucket_day in baseline_days for review in daily.get(bucket_day, [])]
        current_reviews = daily.get(day, [])

        baseline_sentiment = sum(r.get("sentiment_score", 0) for r in baseline_reviews) / max(len(baseline_reviews), 1)
        current_sentiment = sum(r.get("sentiment_score", 0) for r in current_reviews) / max(len(current_reviews), 1)
        delta = round(current_sentiment - baseline_sentiment, 4)

        if delta > settings.SENTIMENT_DROP_THRESHOLD:
            continue

        current_aspects = {item["aspect"]: item for item in aspect_rollup(current_reviews)}
        baseline_aspects = {item["aspect"]: item for item in aspect_rollup(baseline_reviews)}

        degrading = []
        for aspect, current in current_aspects.items():
            previous = baseline_aspects.get(aspect, {"average_score": 0.0, "mention_count": 0})
            degrading.append((
                aspect,
                round(current["average_score"] - previous["average_score"], 4),
                current["mention_count"] - previous["mention_count"],
            ))

        degrading.sort(key=lambda item: (item[1], -item[2]))
        earliest_aspect = degrading[0][0] if degrading else None
        amplification_chain = [item[0] for item in degrading if item[1] <= settings.ASPECT_DROP_THRESHOLD][:3]

        # Get evidence (most negative reviews)
        evidence = []
        for review in sorted(current_reviews, key=lambda r: r.get("sentiment_score", 0))[:5]:
            evidence.append({
                "review_id": str(review.get("_id")),
                "sentiment_score": review.get("sentiment_score"),
                "snippet": (review.get("content") or "")[:180],
                "aspects": [aspect["aspect"] for aspect in review.get("aspect_sentiments", [])],
            })

        event_doc = {
            "user_id": user_id,
            "type": "root_cause",
            "event_date": day,
            "baseline_sentiment": round(baseline_sentiment, 4),
            "current_sentiment": round(current_sentiment, 4),
            "sentiment_delta": delta,
            "review_volume": len(current_reviews),
            "earliest_degrading_aspect": earliest_aspect,
            "amplification_chain": amplification_chain,
            "recommendations": _recommendations_for_aspect(earliest_aspect),
            "evidence": evidence,
            "created_at": datetime.utcnow(),
        }

        result = await db[EVENTS_COLLECTION].insert_one(event_doc)
        event_doc["_id"] = str(result.inserted_id)
        events.append(event_doc)

    # Clear cache
    await cache_delete_pattern(f"root-cause:{user_id}:")

    return events


async def get_root_cause_events(user_id: str) -> List[dict]:
    """Get root cause events for a user"""
    cache_key = f"root-cause:{user_id}:events"

    cached = await cache_get(cache_key)
    if cached is not None:
        return cached

    db = get_mongodb()
    if db is None:
        return []

    query = {"user_id": user_id, "type": "root_cause"}
    cursor = db[EVENTS_COLLECTION].find(query).sort("event_date", -1)
    events = await cursor.to_list(length=100)

    if not events:
        events = await rebuild_root_causes(user_id)

    serialized = [
        {
            "id": str(event.get("_id")),
            "event_date": event.get("event_date").isoformat() if event.get("event_date") else None,
            "baseline_sentiment": event.get("baseline_sentiment"),
            "current_sentiment": event.get("current_sentiment"),
            "sentiment_delta": event.get("sentiment_delta"),
            "review_volume": event.get("review_volume"),
            "earliest_degrading_aspect": event.get("earliest_degrading_aspect"),
            "amplification_chain": event.get("amplification_chain", []),
            "recommendations": event.get("recommendations", []),
            "evidence": event.get("evidence", []),
            "created_at": event.get("created_at").isoformat() if event.get("created_at") else None,
        }
        for event in events
    ]

    await cache_set(cache_key, serialized)
    return serialized
