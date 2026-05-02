"""
SentimentIQ - Anomaly Detection Module
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import numpy as np
from scipy import stats


class AnomalyDetector:
    """Anomaly detection for sentiment drops"""
    
    def __init__(self, threshold: float = 0.3):
        self.threshold = threshold
        self.baseline_sentiment = None
        self.baseline_std = None
    
    def detect(
        self,
        reviews: List[Dict],
        window_hours: int = 24,
        min_reviews: int = 5,
    ) -> List[Dict]:
        """Detect anomalies in sentiment data"""
        if not reviews or len(reviews) < min_reviews:
            return []
        
        anomalies = []
        
        # Group reviews by time window
        reviews_by_window = self._group_by_time_window(reviews, window_hours)
        
        for window_start, window_reviews in reviews_by_window.items():
            if len(window_reviews) < min_reviews:
                continue
            
            # Calculate window sentiment
            scores = [r.get("sentiment_score", 0) for r in window_reviews]
            avg_score = np.mean(scores)
            
            # Check if baseline exists
            if self.baseline_sentiment is None:
                self.baseline_sentiment = avg_score
                self.baseline_std = np.std(scores) or 0.1
                continue
            
            # Detect deviation
            deviation = self.baseline_sentiment - avg_score
            deviation_pct = (deviation / abs(self.baseline_sentiment)) if self.baseline_sentiment != 0 else 0
            
            if abs(deviation) > self.threshold * abs(self.baseline_sentiment) or deviation_pct > self.threshold:
                # Determine severity
                severity = "low"
                if abs(deviation) > self.threshold * 2 * abs(self.baseline_sentiment):
                    severity = "critical"
                elif abs(deviation) > self.threshold * 1.5 * abs(self.baseline_sentiment):
                    severity = "high"
                elif abs(deviation) > self.threshold * abs(self.baseline_sentiment):
                    severity = "medium"
                
                # Create anomaly record
                anomaly = {
                    "anomaly_type": "sentiment_drop" if deviation > 0 else "sentiment_spike",
                    "severity": severity,
                    "title": f"Sentiment {('drop' if deviation > 0 else 'increase')} detected",
                    "description": f"Average sentiment changed by {deviation_pct:.1%} from baseline",
                    "baseline_score": self.baseline_sentiment,
                    "current_score": avg_score,
                    "deviation": deviation,
                    "deviation_percentage": deviation_pct,
                    "start_date": window_start,
                    "affected_reviews": len(window_reviews),
                    "status": "detected",
                    "detected_at": datetime.utcnow(),
                }
                anomalies.append(anomaly)
        
        return anomalies
    
    def _group_by_time_window(
        self,
        reviews: List[Dict],
        window_hours: int,
    ) -> Dict[datetime, List[Dict]]:
        """Group reviews by time window"""
        windows = {}
        
        for review in reviews:
            created_at = review.get("created_at")
            if not created_at:
                continue
            
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            
            # Round to window
            window_start = created_at.replace(
                minute=0, second=0, microsecond=0
            )
            # Align to window boundaries
            window_start = window_start - timedelta(
                minutes=window_start.minute % (window_hours * 60)
            )
            
            if window_start not in windows:
                windows[window_start] = []
            windows[window_start].append(review)
        
        return windows
    
    def get_root_causes(
        self,
        reviews: List[Dict],
        anomaly_id: int,
    ) -> List[Dict]:
        """Identify potential root causes"""
        root_causes = []
        
        if not reviews:
            return root_causes
        
        # Analyze negative reviews for common themes
        negative_reviews = [
            r for r in reviews 
            if r.get("sentiment_label") == "negative"
        ]
        
        if not negative_reviews:
            return root_causes
        
        # Simple keyword-based root cause detection
        cause_keywords = {
            "product_quality": ["quality", "broken", "defective", "damaged", "cheap"],
            "shipping": ["shipping", "delivery", "late", "lost", "arrived"],
            "customer_service": ["service", "support", "response", "helpful", "rude"],
            "price": ["price", "expensive", "cheap", "value", "overpriced"],
            "product_issues": ["doesn't work", "not working", "broken", "failed"],
        }
        
        # Count occurrences
        cause_scores = {cause: 0 for cause in cause_keywords}
        
        for review in negative_reviews:
            content = review.get("content", "").lower()
            for cause, keywords in cause_keywords.items():
                for keyword in keywords:
                    if keyword in content:
                        cause_scores[cause] += 1
        
        # Create root causes for significant matches
        min_count = max(1, len(negative_reviews) * 0.1)
        
        for cause, count in cause_scores.items():
            if count >= min_count:
                root_causes.append({
                    "cause_type": cause,
                    "category": "product" if cause in ["product_quality", "product_issues"] else cause,
                    "title": f"Issues with {cause.replace('_', ' ')}",
                    "description": f"Found in {count} negative reviews",
                    "impact_score": count / len(negative_reviews),
                    "evidence_count": count,
                    "status": "identified",
                    "identified_at": datetime.utcnow().isoformat(),
                })
        
        return root_causes


class RootCauseAnalyzer:
    """Root cause analysis engine"""
    
    def __init__(self):
        self.cause_categories = {
            "product_quality": ["quality", "defective", "broken", "poor quality"],
            "shipping": ["shipping", "delivery", "late delivery", "lost package"],
            "customer_service": ["service", "support", "response time", "unhelpful"],
            "price": ["overpriced", "expensive", "poor value", "overcharged"],
            "product_not_as_described": ["not as described", "different", "smaller", "bigger"],
            "returns": ["return", "refund", "exchange", "money back"],
        }
    
    def analyze(
        self,
        reviews: List[Dict],
        anomaly_id: int,
    ) -> List[Dict]:
        """Analyze root causes for an anomaly"""
        root_causes = []
        
        if not reviews:
            return root_causes
        
        # Get negative reviews in anomaly window
        negative = [r for r in reviews if r.get("sentiment_label") == "negative"]
        
        if not negative:
            return root_causes
        
        # Analyze each category
        for category, keywords in self.cause_categories.items():
            matching = []
            for review in negative:
                content = review.get("content", "").lower()
                for keyword in keywords:
                    if keyword in content:
                        matching.append(review)
                        break
            
            if matching:
                score = len(matching) / len(negative)
                if score >= 0.05:  # At least 5% of negative reviews
                    root_causes.append({
                        "anomaly_id": anomaly_id,
                        "cause_type": category,
                        "category": "product" if "product" in category else category,
                        "title": f"Root cause: {category.replace('_', ' ')}",
                        "impact_score": score,
                        "confidence": min(1.0, score * 2),
                        "evidence_count": len(matching),
                        "status": "identified",
                    })
        
        return root_causes
    
    def generate_recommendations(
        self,
        root_cause: Dict,
    ) -> str:
        """Generate recommendation for a root cause"""
        recommendations = {
            "product_quality": "Review quality control processes and supplier standards.",
            "shipping": "Evaluate shipping partners and consider faster delivery options.",
            "customer_service": "Increase support staff during peak periods.",
            "price": "Review pricing strategy and consider promotional offers.",
            "product_not_as_described": "Update product descriptions with accurate details and photos.",
            "returns": "Simplify return process and improve refund speed.",
        }
        
        return recommendations.get(
            root_cause.get("cause_type"),
            "Review and address the identified issue."
        )
