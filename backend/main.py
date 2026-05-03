from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1 import auth, dashboard, meta, reports, reviews, root_cause, settings as settings_api
from core.config import settings
from db.mongodb import close_mongodb, init_mongodb
from db.redis_cache import close_redis, init_redis
from db.sqlite import init_sqlite


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings.upload_path.mkdir(parents=True, exist_ok=True)
    init_sqlite()
    await init_mongodb()
    await init_redis()
    yield
    await close_mongodb()
    await close_redis()


app = FastAPI(
    title="SentimentIQ API",
    description="Customer review intelligence platform for sentiment diagnostics and root-cause detection.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(meta.router)
app.include_router(auth.router, prefix="/api/v1")
app.include_router(reviews.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")
app.include_router(root_cause.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")
app.include_router(settings_api.router, prefix="/api/v1")


@app.get("/")
async def root() -> dict:
    return {
        "name": settings.APP_NAME,
        "status": "running",
        "generated_at": datetime.utcnow().isoformat(),
        "docs": "/docs",
    }
