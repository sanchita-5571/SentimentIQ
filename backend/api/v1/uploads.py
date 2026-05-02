"""
SentimentIQ - Uploads API (MongoDB version)
"""

import csv
import io
import json
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from api.v1.auth import get_current_active_user
from db.mongodb import get_mongodb
from db.postgres import REVIEWS_COLLECTION

router = APIRouter()


@router.post("/csv")
async def upload_csv(
    file: UploadFile = File(...),
    current_user=Depends(get_current_active_user),
):
    """Upload CSV file"""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    contents = await file.read()
    text = contents.decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))

    created_count = 0
    reviews = []
    for row in reader:
        review_doc = {
            "user_id": current_user.id,
            "source": "csv",
            "external_id": row.get("id") or row.get("review_id"),
            "author": row.get("author"),
            "title": row.get("title"),
            "content": row.get("content") or row.get("review") or row.get("text"),
            "rating": float(row.get("rating")) if row.get("rating") else None,
            "product": row.get("product_name") or row.get("product"),
            "category": row.get("category"),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        if review_doc["content"]:
            review_doc["word_count"] = len(review_doc["content"].split())
            review_doc["char_count"] = len(review_doc["content"])
        reviews.append(review_doc)
        created_count += 1

    if reviews:
        await db[REVIEWS_COLLECTION].insert_many(reviews)

    return {"created": created_count, "source": "csv"}


@router.post("/json")
async def upload_json(
    data: list,
    current_user=Depends(get_current_active_user),
):
    """Import JSON data"""
    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    created_count = 0
    reviews = []

    for item in data:
        review_doc = {
            "user_id": current_user.id,
            "source": "json",
            "external_id": item.get("id"),
            "author": item.get("author"),
            "title": item.get("title"),
            "content": item.get("content") or item.get("review") or item.get("text"),
            "rating": float(item.get("rating")) if item.get("rating") else None,
            "product": item.get("product_name") or item.get("product"),
            "category": item.get("category"),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        if review_doc["content"]:
            review_doc["word_count"] = len(review_doc["content"].split())
            review_doc["char_count"] = len(review_doc["content"])
        reviews.append(review_doc)
        created_count += 1

    if reviews:
        await db[REVIEWS_COLLECTION].insert_many(reviews)

    return {"created": created_count, "source": "json"}


@router.post("/manual")
async def manual_input(
    content: str,
    rating: Optional[float] = None,
    product: Optional[str] = None,
    category: Optional[str] = None,
    title: Optional[str] = None,
    current_user=Depends(get_current_active_user),
):
    """Manual text input"""
    if not content:
        raise HTTPException(status_code=400, detail="Content is required")

    db = get_mongodb()
    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    word_count = len(content.split())
    char_count = len(content)

    review_doc = {
        "user_id": current_user.id,
        "source": "manual",
        "title": title,
        "content": content,
        "rating": rating,
        "product": product,
        "category": category,
        "word_count": word_count,
        "char_count": char_count,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    result = await db[REVIEWS_COLLECTION].insert_one(review_doc)

    return {"id": str(result.inserted_id), "message": "Review added successfully"}


@router.get("/sources")
async def get_enabled_sources(
    current_user=Depends(get_current_active_user),
):
    """Get enabled data sources"""
    return {
        "csv": True,
        "json": True,
        "manual": True,
    }
