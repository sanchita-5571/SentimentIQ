from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from db.mongodb import get_mongodb

HISTORY_COLLECTION = "dashboard_snapshot_history"


async def store_dashboard_snapshot_history(
    user_id: str,
    *,
    batch_id: Optional[str],
    filters: dict[str, Any],
    snapshot: dict[str, Any],
    root_causes: list[Any],
) -> dict[str, Any]:
    db = get_mongodb()
    if db is None:
        raise RuntimeError("MongoDB not connected")

    doc = {
        "user_id": user_id,
        "batch_id": batch_id,
        "filters": filters,
        "snapshot": snapshot,
        "root_causes": root_causes,
        "created_at": datetime.utcnow().isoformat(),
    }

    result = await db[HISTORY_COLLECTION].insert_one(doc)
    return {
        "id": str(result.inserted_id),
        "created_at": doc["created_at"],
    }


async def list_dashboard_snapshot_history(
    user_id: str,
    *,
    search: Optional[str] = None,
    limit: int = 50,
) -> list[dict[str, Any]]:
    db = get_mongodb()
    if db is None:
        return []

    query: dict[str, Any] = {"user_id": user_id}

    if search:
        # Best-effort search across some stringified fields
        query["$or"] = [
            {"batch_id": {"$regex": search, "$options": "i"}},
            {"filters.search": {"$regex": search, "$options": "i"}},
        ]

    cursor = (
        db[HISTORY_COLLECTION]
        .find(query)
        .sort("created_at", -1)
        .limit(max(1, min(limit, 100)))
    )

    docs = await cursor.to_list(length=max(1, min(limit, 100)))
    result: list[dict[str, Any]] = []
    for d in docs:
        result.append(
            {
                "id": str(d.get("_id")),
                "batch_id": d.get("batch_id"),
                "filters": d.get("filters") or {},
                "snapshot": d.get("snapshot"),
                "root_causes": d.get("root_causes") or [],
                "created_at": d.get("created_at"),
            }
        )
    return result

