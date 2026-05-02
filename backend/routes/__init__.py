"""
SentimentIQ - Routes Module
"""

from .alert_routes import router as alert_router
from .anomaly_routes import router as anomaly_router
from .aspect_routes import router as aspect_router
from .brand_routes import router as brand_router
from .recommendation_routes import router as recommendation_router
from .review_routes import router as review_router
from .sentiment_routes import router as sentiment_router
from .topic_routes import router as topic_router

__all__ = [
    "alert_router",
    "anomaly_router",
    "aspect_router",
    "brand_router",
    "recommendation_router",
    "review_router",
    "sentiment_router",
    "topic_router",
]