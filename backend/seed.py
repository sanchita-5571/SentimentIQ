import asyncio
import json

from core.config import settings
from db.mongodb import init_mongodb
from db.redis_cache import init_redis
from db.sqlite import SessionLocal, init_sqlite
from db.sql_models import UserRecord
from services.review_ingestion_service import ingest_reviews, normalize_review_row, parse_csv_bytes


async def run_seed() -> None:
    init_sqlite()
    await init_mongodb()
    await init_redis()

    with SessionLocal() as session:
        analyst = session.query(UserRecord).filter(UserRecord.email == settings.DEMO_USER_EMAIL).first()
        if analyst is None:
            raise RuntimeError("Demo analyst user was not created")
        user_id = analyst.id

    sample_csv = (settings.backend_dir / settings.DEFAULT_SAMPLE_CSV).resolve()
    sample_json = (settings.backend_dir / settings.DEFAULT_SAMPLE_JSON).resolve()
    if not sample_csv.exists():
        raise FileNotFoundError(sample_csv)
    if not sample_json.exists():
        raise FileNotFoundError(sample_json)

    csv_rows = parse_csv_bytes(sample_csv.read_bytes())
    json_rows = json.loads(sample_json.read_text(encoding="utf-8"))
    json_reviews = json_rows if isinstance(json_rows, list) else json_rows.get("reviews", [])

    csv_result = await ingest_reviews(user_id, [normalize_review_row(row, "csv") for row in csv_rows], "seed-csv")
    json_result = await ingest_reviews(user_id, [normalize_review_row(row, "json") for row in json_reviews], "seed-json")

    print(
        "Seed complete: "
        f"csv_created={csv_result['created_count']} "
        f"json_created={json_result['created_count']} "
        f"duplicates={csv_result['duplicate_count'] + json_result['duplicate_count']}"
    )


if __name__ == "__main__":
    asyncio.run(run_seed())
