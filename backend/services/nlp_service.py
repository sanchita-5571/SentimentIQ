import math
import re
from collections import Counter, defaultdict
from functools import lru_cache

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from core.config import settings

try:
    from langdetect import detect as detect_language_code
except Exception:
    detect_language_code = None


ASPECT_KEYWORDS = {
    "shipping": ["shipping", "delivery", "courier", "arrived", "late", "delay"],
    "quality": ["quality", "broken", "damaged", "defect", "durable", "crack"],
    "support": ["support", "service", "agent", "refund", "response", "help"],
    "pricing": ["price", "pricing", "discount", "expensive", "cost", "value"],
    "packaging": ["packaging", "box", "seal", "wrapped", "unboxing"],
    "usability": ["setup", "install", "manual", "instructions", "app", "experience"],
}

TOPIC_KEYWORDS = {
    "delivery delays": ["late", "delay", "shipping", "arrived", "delivery"],
    "product defects": ["broken", "damaged", "defect", "crack", "faulty"],
    "refund friction": ["refund", "return", "support", "service", "agent"],
    "pricing pressure": ["expensive", "price", "cost", "discount", "value"],
    "onboarding issues": ["setup", "install", "manual", "instructions", "login"],
}


@lru_cache(maxsize=1)
def get_vader() -> SentimentIntensityAnalyzer:
    return SentimentIntensityAnalyzer()


@lru_cache(maxsize=1)
def get_transformer_pipeline():
    if not settings.ENABLE_TRANSFORMERS:
        return None
    try:
        from transformers import pipeline

        return pipeline("sentiment-analysis", model=settings.TRANSFORMER_MODEL)
    except Exception:
        return None


def clean_text(text: str) -> str:
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"[^A-Za-z0-9\s'.,!?-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalized_hash(text: str) -> str:
    import hashlib

    normalized = re.sub(r"\s+", " ", clean_text(text).lower()).strip()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def detect_language(text: str) -> str:
    if not text.strip():
        return "unknown"
    if detect_language_code is None:
        return "en"
    try:
        return detect_language_code(text)
    except Exception:
        return "unknown"


def _transformer_score(text: str) -> tuple[float, float] | None:
    classifier = get_transformer_pipeline()
    if classifier is None:
        return None
    result = classifier(text[:512])[0]
    confidence = float(result["score"])
    score = confidence if result["label"].upper() == "POSITIVE" else -confidence
    return score, confidence


def classify_sentiment(text: str, language: str) -> tuple[float, str, float]:
    vader_score = get_vader().polarity_scores(text)["compound"]
    transformer_result = _transformer_score(text) if language == "en" else None

    if transformer_result is not None:
        score = (vader_score + transformer_result[0]) / 2
        confidence = max(abs(score), transformer_result[1])
    else:
        score = vader_score
        confidence = max(abs(vader_score), 0.51)

    if score <= settings.VADER_NEGATIVE_THRESHOLD:
        label = "negative"
    elif score >= settings.VADER_POSITIVE_THRESHOLD:
        label = "positive"
    else:
        label = "neutral"

    return round(float(score), 4), label, round(float(min(confidence, 1.0)), 4)


def extract_aspects(text: str) -> list[dict]:
    lower_text = text.lower()
    aspects = []
    analyzer = get_vader()
    for aspect, keywords in ASPECT_KEYWORDS.items():
        matched = [keyword for keyword in keywords if keyword in lower_text]
        if not matched:
            continue
        aspect_score = analyzer.polarity_scores(text)["compound"]
        aspects.append(
            {
                "aspect": aspect,
                "score": round(float(aspect_score), 4),
                "mentions": len(matched),
                "keywords": matched,
            }
        )
    if not aspects:
        aspects.append(
            {
                "aspect": "general",
                "score": round(float(analyzer.polarity_scores(text)["compound"]), 4),
                "mentions": 1,
                "keywords": [],
            }
        )
    return aspects


def extract_topics(texts: list[str]) -> list[list[str]]:
    texts = [clean_text(text) for text in texts]
    if not texts:
        return []

    if settings.ENABLE_BERTOPIC and len(texts) >= settings.BERTOPIC_MIN_REVIEWS:
        try:
            from bertopic import BERTopic

            model = BERTopic(verbose=False, calculate_probabilities=False)
            labels, _ = model.fit_transform(texts)
            topic_info = model.get_topic_info().set_index("Topic")["Name"].to_dict()
            return [[topic_info.get(label, "other")] for label in labels]
        except Exception:
            pass

    derived_topics: list[list[str]] = []
    for text in texts:
        lower_text = text.lower()
        matched_topics = [
            topic for topic, keywords in TOPIC_KEYWORDS.items() if any(word in lower_text for word in keywords)
        ]
        if not matched_topics:
            tokens = [token for token in re.findall(r"[a-zA-Z]{4,}", lower_text) if token not in {"this", "that", "with", "from", "have"}]
            common = Counter(tokens).most_common(2)
            matched_topics = [" ".join(word for word, _ in common)] if common else ["general feedback"]
        derived_topics.append(matched_topics[:2])
    return derived_topics


def build_recommendation_tags(aspects: list[dict], sentiment_label: str) -> list[str]:
    if sentiment_label != "negative":
        return ["monitor"]
    ordered = sorted(aspects, key=lambda aspect: aspect["score"])
    tags = [aspect["aspect"] for aspect in ordered[:3]]
    return tags or ["general"]


def aspect_rollup(reviews: list) -> list[dict]:
    buckets: dict[str, dict[str, float]] = defaultdict(lambda: {"total_score": 0.0, "mentions": 0.0})
    for review in reviews:
        for aspect in review.get("aspect_sentiments", []) or []:
            buckets[aspect["aspect"]]["total_score"] += float(aspect["score"])
            buckets[aspect["aspect"]]["mentions"] += float(aspect["mentions"])
    results = []
    for aspect, values in buckets.items():
        mentions = int(values["mentions"])
        avg_score = values["total_score"] / mentions if mentions else 0.0
        results.append({"aspect": aspect, "average_score": round(avg_score, 4), "mention_count": mentions})
    return sorted(results, key=lambda item: (item["average_score"], -item["mention_count"]))


def topic_rollup(reviews: list) -> list[dict]:
    stats: dict[str, dict[str, float]] = defaultdict(lambda: {"mentions": 0, "sentiment_total": 0.0})
    for review in reviews:
        for topic in review.get("topics", []) or []:
            stats[topic]["mentions"] += 1
            stats[topic]["sentiment_total"] += review.get("sentiment_score", 0.0)
    output = []
    for topic, values in stats.items():
        mentions = int(values["mentions"])
        avg_sentiment = values["sentiment_total"] / mentions if mentions else 0.0
        output.append({"topic": topic, "mentions": mentions, "avg_sentiment": round(avg_sentiment, 4)})
    return sorted(output, key=lambda item: (-item["mentions"], item["avg_sentiment"]))
