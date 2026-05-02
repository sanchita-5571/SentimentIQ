"""
SentimentIQ - Reports API (MongoDB version)
"""

import csv
import io
import json
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from api.v1.auth import get_current_user
from db.mongodb import get_mongodb
from db.postgres import REVIEWS_COLLECTION
from db.sql_models import ReportExportRecord
from db.sqlite import get_db_session
from schemas.report import ReportExportRequest

router = APIRouter(prefix="/reports", tags=["reports"])


def build_filter_query(
    user_id: str,
    source: Optional[str] = None,
    product: Optional[str] = None,
    category: Optional[str] = None,
    sentiment_label: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> dict:
    """Build MongoDB filter query"""
    query = {"user_id": user_id}

    if source:
        query["source"] = source
    if product:
        query["product"] = product
    if category:
        query["category"] = category
    if sentiment_label:
        query["sentiment_label"] = sentiment_label
    if start_date or end_date:
        query["review_date"] = {}
        if start_date:
            query["review_date"]["$gte"] = start_date
        if end_date:
            query["review_date"]["$lte"] = end_date

    return query


@router.post("/export")
async def export_report(
    payload: ReportExportRequest,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db_session),
):
    """Export report in various formats"""
    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    query = build_filter_query(
        user_id=current_user.id,
        source=payload.source,
        product=payload.product,
        category=payload.category,
        sentiment_label=payload.sentiment_label,
        start_date=payload.start_date,
        end_date=payload.end_date,
    )

    # Get reviews
    cursor = db[REVIEWS_COLLECTION].find(query).sort("review_date", -1)
    reviews = await cursor.to_list(length=10000)

    # Get overview stats
    total_reviews = len(reviews)
    total_sentiment = sum(r.get("sentiment_score", 0) for r in reviews)
    negative_count = sum(1 for r in reviews if r.get("sentiment_label") == "negative")

    overview = {
        "total_reviews": total_reviews,
        "average_sentiment": total_sentiment / total_reviews if total_reviews > 0 else 0.0,
        "negative_ratio": negative_count / total_reviews if total_reviews > 0 else 0.0,
    }

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    export_format = payload.format

    session.add(
        ReportExportRecord(
            user_id=current_user.id,
            export_format=export_format,
            filters_json=payload.model_dump_json(),
            created_at=datetime.utcnow(),
        )
    )
    session.commit()

    if export_format == "json":
        export_payload = {
            "generated_at": datetime.utcnow().isoformat(),
            "snapshot": {"overview": overview},
            "reviews": [
                {
                    "id": str(review["_id"]),
                    "content": review.get("content"),
                    "sentiment_label": review.get("sentiment_label"),
                    "sentiment_score": review.get("sentiment_score"),
                    "topics": review.get("topics", []),
                    "aspects": review.get("aspect_sentiments", []),
                }
                for review in reviews
            ],
        }
        stream = io.BytesIO(json.dumps(export_payload, indent=2).encode("utf-8"))
        return StreamingResponse(
            stream,
            media_type="application/json",
            headers={"Content-Disposition": f'attachment; filename="sentimentiq-report-{timestamp}.json"'},
        )

    if export_format == "markdown":
        lines = [
            "# SentimentIQ Report",
            "",
            f"- Generated at: {datetime.utcnow().isoformat()}",
            f"- Total reviews: {overview['total_reviews']}",
            f"- Average sentiment: {overview['average_sentiment']}",
            f"- Negative ratio: {overview['negative_ratio']}",
            "",
            "## Recent negative verbatims",
        ]
        for review in [r for r in reviews if r.get("sentiment_label") == "negative"][:10]:
            content = review.get("content", "")[:160]
            lines.append(f"- #{review['_id']} {content}")
        content = "\n".join(lines).encode("utf-8")
        return StreamingResponse(
            io.BytesIO(content),
            media_type="text/markdown",
            headers={"Content-Disposition": f'attachment; filename="sentimentiq-report-{timestamp}.md"'},
        )

    if export_format != "csv":
        raise HTTPException(status_code=400, detail="Supported formats: csv, json, markdown")

    stream = io.StringIO()
    writer = csv.writer(stream)
    writer.writerow(["id", "date", "source", "product", "rating", "sentiment_label", "sentiment_score", "topics", "content"])
    for review in reviews:
        writer.writerow([
            str(review.get("_id")),
            (review.get("review_date") or datetime.utcnow()).isoformat(),
            review.get("source"),
            review.get("product"),
            review.get("rating"),
            review.get("sentiment_label"),
            review.get("sentiment_score"),
            ", ".join(review.get("topics", []) or []),
            review.get("content"),
        ])
    return StreamingResponse(
        io.BytesIO(stream.getvalue().encode("utf-8")),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="sentimentiq-report-{timestamp}.csv"'},
    )
