from datetime import datetime, timedelta
from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from api.v1.auth import get_current_user
from db.mongodb import get_mongodb
from db.postgres import REVIEWS_COLLECTION, INGESTION_BATCHES_COLLECTION
from db.redis_cache import cache_delete_pattern
from schemas.batch import ReviewBatchActionResponse, ReviewBatchMetadata, ReviewBatchUpdateRequest
from schemas.review import IngestionResponse, ReviewListResponse, ReviewResponse
from services.nlp_service import (
    build_recommendation_tags,
    classify_sentiment,
    clean_text,
    detect_language,
    extract_aspects,
    extract_topics,
    get_vader,
)
from services.review_ingestion_service import ingest_reviews, normalize_review_row, parse_csv_bytes, parse_json_bytes

router = APIRouter(prefix="/reviews", tags=["reviews"])


def serialize_review(doc: dict) -> dict:
    return {
        "id": str(doc.get("_id")),
        "source": doc.get("source", "csv"),
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
    batch_id: Optional[str] = None,
) -> dict:
    """Build MongoDB filter query"""
    query = {"user_id": user_id}
    normalized_end_date = end_date

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
    if batch_id:
        query["batch_id"] = batch_id
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
    batch_id: Optional[str] = None,
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
        batch_id=batch_id,
    )

    skip = (page - 1) * page_size
    total = await db[REVIEWS_COLLECTION].count_documents(query)
    items_cursor = db[REVIEWS_COLLECTION].find(query).sort("review_date", -1).skip(skip).limit(page_size)
    items = await items_cursor.to_list(length=page_size)

    reviews = [ReviewResponse(**serialize_review(doc)) for doc in items]

    return ReviewListResponse(items=reviews, total=total, page=page, page_size=page_size)





@router.post("/upload/csv", response_model=IngestionResponse)
async def upload_csv_reviews(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
) -> dict:
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported here")
    rows = await parse_csv_bytes(await file.read())
    reviews = [normalize_review_row(row, "csv") for row in rows]
    return await ingest_reviews(
        current_user.id,
        reviews,
        "csv",
        {"file_name": file.filename, "metadata_json": {"content_type": file.content_type}},
    )


@router.post("/upload/json", response_model=IngestionResponse)
async def upload_json_reviews(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
) -> dict:
    if not file.filename.lower().endswith(".json"):
        raise HTTPException(status_code=400, detail="Only JSON files are supported here")
    rows = parse_json_bytes(await file.read())
    reviews = [normalize_review_row(row, "json") for row in rows]
    return await ingest_reviews(
        current_user.id,
        reviews,
        "json",
        {"file_name": file.filename, "metadata_json": {"content_type": file.content_type}},
    )


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


@router.get("/batches", response_model=list[ReviewBatchMetadata])
async def list_review_batches(
    search: Optional[str] = None,
    current_user=Depends(get_current_user),
) -> list[ReviewBatchMetadata]:
    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    query = {"user_id": current_user.id}
    if search:
        query["$or"] = [
            {"file_name": {"$regex": search, "$options": "i"}},
            {"source": {"$regex": search, "$options": "i"}},
        ]

    cursor = db[INGESTION_BATCHES_COLLECTION].find(query).sort("created_at", -1)
    batches = await cursor.to_list(length=100)
    return [ReviewBatchMetadata(**batch) for batch in batches]


@router.get("/batches/{batch_id}", response_model=ReviewBatchMetadata)
async def get_review_batch(
    batch_id: str,
    current_user=Depends(get_current_user),
) -> ReviewBatchMetadata:
    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    batch = await db[INGESTION_BATCHES_COLLECTION].find_one({"user_id": current_user.id, "batch_id": batch_id})
    if batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")
    return ReviewBatchMetadata(**batch)


@router.put("/batches/{batch_id}", response_model=ReviewBatchMetadata)
async def update_review_batch(
    batch_id: str,
    payload: ReviewBatchUpdateRequest,
    current_user=Depends(get_current_user),
) -> ReviewBatchMetadata:
    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    update_fields = {}
    if payload.file_name is not None:
        update_fields["file_name"] = payload.file_name
    if payload.metadata_json is not None:
        update_fields["metadata_json"] = payload.metadata_json
    if update_fields:
        await db[INGESTION_BATCHES_COLLECTION].update_one(
            {"user_id": current_user.id, "batch_id": batch_id},
            {"$set": update_fields},
        )

    batch = await db[INGESTION_BATCHES_COLLECTION].find_one({"user_id": current_user.id, "batch_id": batch_id})
    if batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")
    return ReviewBatchMetadata(**batch)


@router.delete("/batches/{batch_id}")
async def delete_review_batch(
    batch_id: str,
    current_user=Depends(get_current_user),
) -> dict:
    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    review_query = {"user_id": current_user.id, "batch_id": batch_id}
    deleted_reviews = await db[REVIEWS_COLLECTION].delete_many(review_query)
    deleted_batch = await db[INGESTION_BATCHES_COLLECTION].delete_one({"user_id": current_user.id, "batch_id": batch_id})
    await cache_delete_pattern(f"dashboard:{current_user.id}:")
    await cache_delete_pattern(f"root-cause:{current_user.id}:")
    return {
        "deleted_reviews": deleted_reviews.deleted_count if hasattr(deleted_reviews, "deleted_count") else 0,
        "deleted_batch": deleted_batch.deleted_count if hasattr(deleted_batch, "deleted_count") else 0,
    }


@router.post("/batches/{batch_id}/rerun", response_model=ReviewBatchActionResponse)
async def rerun_review_batch(
    batch_id: str,
    current_user=Depends(get_current_user),
) -> ReviewBatchActionResponse:
    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    reviews = await db[REVIEWS_COLLECTION].find({"user_id": current_user.id, "batch_id": batch_id}).to_list(length=10000)
    if not reviews:
        raise HTTPException(status_code=404, detail="Batch not found")

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

    reprocessed_count = 0
    for index, review in enumerate(reviews):
        if not review.get("_id"):
            continue
        sentiment_score, sentiment_label, sentiment_confidence = sentiments[index]
        aspect_sentiments = aspects_list[index]
        await db[REVIEWS_COLLECTION].update_one(
            {"_id": review["_id"], "user_id": current_user.id},
            {
                "$set": {
                    "sentiment_score": sentiment_score,
                    "sentiment_label": sentiment_label,
                    "sentiment_confidence": sentiment_confidence,
                    "aspect_sentiments": aspect_sentiments,
                    "recommendation_tags": build_recommendation_tags(aspect_sentiments, sentiment_label),
                    "topics": all_topics[index],
                    "topic_cluster": all_topics[index][0] if all_topics[index] else "general feedback",
                    "updated_at": datetime.utcnow(),
                }
            },
        )
        reprocessed_count += 1

    await cache_delete_pattern(f"dashboard:{current_user.id}:")
    await cache_delete_pattern(f"root-cause:{current_user.id}:")
    return ReviewBatchActionResponse(
        batch_id=batch_id,
        created_count=len(reviews),
        duplicate_count=0,
        processed_count=reprocessed_count,
        message="Batch rerun completed",
    )
