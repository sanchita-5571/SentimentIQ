"""
SentimentIQ - Sentiments API (MongoDB version)
"""

import json
from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.v1.auth import get_current_active_user
from core.config import settings
from db.mongodb import get_mongodb
from db.postgres import REVIEWS_COLLECTION
from ml.sentiment import SentimentAnalyzer

router = APIRouter()

# Initialize sentiment analyzer
sentiment_analyzer = SentimentAnalyzer()


@router.post("/analyze")
async def analyze_sentiment(
    text: str,
    return_aspects: bool = True,
    return_emotions: bool = True,
):
    """Analyze sentiment of a single text"""
    result = sentiment_analyzer.analyze(
        text,
        return_aspects=return_aspects,
        return_emotions=return_emotions,
    )
    return result


@router.post("/analyze/bulk")
async def analyze_sentiment_bulk(
    review_ids: List[str],
    current_user=Depends(get_current_active_user),
):
    """Analyze sentiment for multiple reviews"""
    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    results = []
    failed = 0

    for review_id in review_ids:
        try:
            doc = await db[REVIEWS_COLLECTION].find_one({"_id": ObjectId(review_id), "user_id": current_user.id})
        except Exception:
            failed += 1
            continue

        if not doc:
            failed += 1
            continue

        # Analyze sentiment
        analysis = sentiment_analyzer.analyze(
            doc.get("content", ""),
            return_aspects=True,
            return_emotions=True,
        )

        # Update review with sentiment
        await db[REVIEWS_COLLECTION].update_one(
            {"_id": ObjectId(review_id)},
            {"$set": {
                "sentiment_score": analysis["sentiment_score"],
                "sentiment_label": analysis["sentiment_label"],
                "sentiment_confidence": analysis["sentiment_confidence"],
                "processed_at": datetime.utcnow(),
            }}
        )

        results.append({"review_id": review_id, "sentiment": analysis["sentiment_label"]})

    return {"processed": len(results), "failed": failed, "results": results}


@router.get("/timeline")
async def get_sentiment_timeline(
    date_from: datetime,
    date_to: datetime,
    interval: str = "day",
    current_user=Depends(get_current_active_user),
):
    """Get sentiment timeline data"""
    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    query = {
        "user_id": current_user.id,
        "review_date": {"$gte": date_from, "$lte": date_to},
        "sentiment_score": {"$ne": None},
    }

    cursor = db[REVIEWS_COLLECTION].find(query)
    reviews = await cursor.to_list(length=10000)

    # Group by time interval
    timeline = {}
    for review in reviews:
        created_at = review.get("created_at") or review.get("review_date")
        if not created_at:
            continue

        if interval == "hour":
            key = created_at.strftime("%Y-%m-%d %H:00")
        elif interval == "day":
            key = created_at.strftime("%Y-%m-%d")
        elif interval == "week":
            key = created_at.strftime("%Y-W%W")
        else:
            key = created_at.strftime("%Y-%m")

        if key not in timeline:
            timeline[key] = {"count": 0, "total": 0, "positive": 0, "negative": 0, "neutral": 0}

        timeline[key]["count"] += 1
        timeline[key]["total"] += review.get("sentiment_score") or 0
        sentiment_label = review.get("sentiment_label")
        if sentiment_label == "positive":
            timeline[key]["positive"] += 1
        elif sentiment_label == "negative":
            timeline[key]["negative"] += 1
        else:
            timeline[key]["neutral"] += 1

    # Calculate averages
    data = []
    for date, stats in sorted(timeline.items()):
        data.append({
            "date": date,
            "avg_sentiment": stats["total"] / stats["count"] if stats["count"] > 0 else 0,
            "review_count": stats["count"],
            "positive_count": stats["positive"],
            "negative_count": stats["negative"],
            "neutral_count": stats["neutral"],
        })

    return data


@router.get("/stats")
async def get_sentiment_stats(
    current_user=Depends(get_current_active_user),
):
    """Get overall sentiment statistics"""
    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    query = {"user_id": current_user.id, "sentiment_score": {"$ne": None}}

    # Total reviews with sentiment
    total = await db[REVIEWS_COLLECTION].count_documents(query)

    # Sentiment distribution
    positive = await db[REVIEWS_COLLECTION].count_documents({**query, "sentiment_label": "positive"})
    negative = await db[REVIEWS_COLLECTION].count_documents({**query, "sentiment_label": "negative"})
    neutral = await db[REVIEWS_COLLECTION].count_documents({**query, "sentiment_label": "neutral"})

    # Average sentiment score and rating (using aggregation would be better)
    cursor = db[REVIEWS_COLLECTION].find(query)
    reviews = await cursor.to_list(length=10000)

    total_sentiment = sum(r.get("sentiment_score", 0) for r in reviews)
    total_rating = sum(r.get("rating", 0) for r in reviews if r.get("rating") is not None)

    return {
        "total_reviews": total,
        "positive_count": positive,
        "negative_count": negative,
        "neutral_count": neutral,
        "positive_percentage": (positive / total * 100) if total > 0 else 0,
        "negative_percentage": (negative / total * 100) if total > 0 else 0,
        "neutral_percentage": (neutral / total * 100) if total > 0 else 0,
        "avg_sentiment": total_sentiment / total if total > 0 else 0.0,
        "avg_rating": total_rating / len([r for r in reviews if r.get("rating") is not None]) if len([r for r in reviews if r.get("rating") is not None]) > 0 else 0.0,
    }


@router.get("/top-issues")
async def get_top_issues(
    limit: int = 10,
    current_user=Depends(get_current_active_user),
):
    """Get top sentiment issues"""
    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    query = {"user_id": current_user.id, "sentiment_label": "negative"}
    cursor = db[REVIEWS_COLLECTION].find(query).sort("sentiment_score", 1).limit(limit)
    reviews = await cursor.to_list(length=limit)

    issues = []
    for review in reviews:
        content = review.get("content", "")
        issues.append({
            "review_id": str(review["_id"]),
            "content": content[:200] + "..." if len(content) > 200 else content,
            "sentiment_score": review.get("sentiment_score"),
            "product": review.get("product"),
            "category": review.get("category"),
            "created_at": (review.get("created_at") or review.get("review_date")).isoformat() if review.get("created_at") or review.get("review_date") else None,
        })

    return issues
