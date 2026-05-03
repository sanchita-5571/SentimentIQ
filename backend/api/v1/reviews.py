from datetime import datetime, timedelta
from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from api.v1.auth import get_current_user
from db.mongodb import get_mongodb
from db.postgres import REVIEWS_COLLECTION
from schemas.review import IngestionResponse, ManualReviewBatch, ReviewListResponse, ReviewResponse
from services.review_ingestion_service import ingest_reviews, normalize_review_row, parse_csv_bytes, parse_json_bytes

router = APIRouter(prefix="/reviews", tags=["reviews"])


def serialize_review(doc: dict) -> dict:
    return {
        "id": str(doc.get("_id")),
        "source": doc.get("source", "manual"),
        "author": doc.get("author"),
        "title": doc.get("title"),
        "content": doc.get("content", ""),
        "language": doc.get("language", "unknown"),
        "rating": doc.get("rating"),
        "product": doc.get("product"),
        "category": doc.get("category"),
        "sentiment_score": doc.get("sentiment_score", 0.0),
        "sentiment_label": doc.get("sentiment_label", "neutral"),
        "sentiment_confidence": doc.get("sentiment_confidence", 0.5),
        "aspect_sentiments": doc.get("aspect_sentiments", []),
        "topics": doc.get("topics", []),
        "topic_cluster": doc.get("topic_cluster"),
        "recommendation_tags": doc.get("recommendation_tags", []),
        "is_duplicate": doc.get("is_duplicate", False),
        "review_date": doc.get("review_date"),
        "created_at": doc.get("created_at"),
    }


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
    """Build MongoDB filter query"""
    query = {"user_id": user_id}
    normalized_end_date = end_date
    # Treat date-only end filters as inclusive so selecting a day includes the full day's reviews.
    if normalized_end_date and normalized_end_date.time() == datetime.min.time():
        normalized_end_date = normalized_end_date + timedelta(days=1) - timedelta(microseconds=1)

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
        if normalized_end_date:
            query["review_date"]["$lte"] = normalized_end_date
    return query


@router.get("", response_model=ReviewListResponse)
async def list_reviews(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    source: Optional[str] = None,
    product: Optional[str] = None,
    category: Optional[str] = None,
    sentiment_label: Optional[str] = None,
    language: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user=Depends(get_current_user),
) -> ReviewListResponse:
    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    query = build_filter_query(
        user_id=current_user.id,
        search=search,
        source=source,
        product=product,
        category=category,
        sentiment_label=sentiment_label,
        language=language,
        start_date=start_date,
        end_date=end_date,
    )

    skip = (page - 1) * page_size
    total = await db[REVIEWS_COLLECTION].count_documents(query)
    items_cursor = db[REVIEWS_COLLECTION].find(query).sort("review_date", -1).skip(skip).limit(page_size)
    items = await items_cursor.to_list(length=page_size)

    # Convert MongoDB documents to Review models
    reviews = [ReviewResponse(**serialize_review(doc)) for doc in items]

    return ReviewListResponse(items=reviews, total=total, page=page, page_size=page_size)


@router.post("/manual", response_model=IngestionResponse)
async def create_manual_reviews(
    payload: ManualReviewBatch,
    current_user=Depends(get_current_user),
) -> dict:
    return await ingest_reviews(current_user.id, payload.reviews, "manual")


@router.post("/upload/csv", response_model=IngestionResponse)
async def upload_csv_reviews(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
) -> dict:
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported here")
    rows = await parse_csv_bytes(await file.read())
    reviews = [normalize_review_row(row, "csv") for row in rows]
    return await ingest_reviews(current_user.id, reviews, "csv")


@router.post("/upload/json", response_model=IngestionResponse)
async def upload_json_reviews(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
) -> dict:
    if not file.filename.lower().endswith(".json"):
        raise HTTPException(status_code=400, detail="Only JSON files are supported here")
    rows = parse_json_bytes(await file.read())
    reviews = [normalize_review_row(row, "json") for row in rows]
    return await ingest_reviews(current_user.id, reviews, "json")


@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(
    review_id: str,
    current_user=Depends(get_current_user),
) -> ReviewResponse:
    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    try:
        doc = await db[REVIEWS_COLLECTION].find_one({"_id": ObjectId(review_id), "user_id": current_user.id})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid review ID")

    if doc is None:
        raise HTTPException(status_code=404, detail="Review not found")

    return ReviewResponse(**serialize_review(doc))
