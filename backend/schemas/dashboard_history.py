from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field

from schemas.dashboard import DashboardSnapshot


class DashboardHistoryCreateRequest(BaseModel):
    batch_id: Optional[str] = None
    filters: dict[str, Any] = Field(default_factory=dict)
    snapshot: DashboardSnapshot
    root_causes: list[Any] = Field(default_factory=list)


class DashboardHistoryEntry(BaseModel):
    id: str = Field(..., description="Mongo document id")
    batch_id: Optional[str] = None
    filters: dict[str, Any] = Field(default_factory=dict)
    snapshot: DashboardSnapshot
    root_causes: list[Any] = Field(default_factory=list)
    created_at: datetime

