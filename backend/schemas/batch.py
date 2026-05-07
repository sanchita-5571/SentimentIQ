from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ReviewBatchMetadata(BaseModel):
    batch_id: str
    source: str
    file_name: str | None = None
    metadata_json: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    created_count: int
    duplicate_count: int
    processed_count: int


class ReviewBatchUpdateRequest(BaseModel):
    file_name: str | None = None
    metadata_json: dict[str, Any] | None = None


class ReviewBatchActionResponse(BaseModel):
    batch_id: str
    created_count: int
    duplicate_count: int
    processed_count: int
    message: str | None = None
