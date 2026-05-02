"""
SentimentIQ - Sentiment Analysis Module
"""

import json
from typing import Dict, List, Optional

import numpy as np


class SentimentAnalyzer:
    """Sentiment analyzer using VADER and transformers"""
    
    def __init__(self):
        self.vader_available = False
        self.transformer_available = False
        self.bertopic_available = False
        self.spacy_available = False
        
        # Try to import VADER
        try:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            self.vader = SentimentIntensityAnalyzer()
            self.vader_available = True
        except ImportError:
            print("VADER not available, using fallback")
        
        # Try to import transformers
        try:
            from transformers import pipeline
            self.transformer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
            self.transformer_available = True
        except ImportError:
            print("Transformers not available, using fallback")
        
        # Try to import BERTopic
        try:
            from bertopic import BERTopic
            self.bertopic_available = True
        except ImportError:
            print("BERTopic not available")
        
        # Try to import spaCy
        try:
            import spacy
            self.nlp = spacy.load("en_core_web_sm")
            self.spacy_available = True
        except:
            print("spaCy not available, aspect extraction disabled")
    
    def analyze(
        self,
        text: str,
        return_aspects: bool = True,
        return_emotions: bool = True,
    ) -> Dict:
        """Analyze sentiment of text"""
        result = {
            "text": text,
            "sentiment_score": 0.0,
            "sentiment_label": "neutral",
            "sentiment_confidence": 0.0,
            "vader": {},
            "transformer": {},
            "aspects": [],
            "emotions": [],
            "topics": [],
        }
        
        if not text or not text.strip():
            return result
        
        # VADER analysis
        if self.vader_available:
            vader_scores = self.vader.polarity_scores(text)
            result["vader"] = {
                "positive": vader_scores["pos"],
                "negative": vader_scores["neg"],
                "neutral": vader_scores["neu"],
                "compound": vader_scores["compound"],
            }
            # Use compound score
            vader_compound = vader_scores["compound"]
            if vader_compound >= 0.05:
                result["sentiment_score"] = vader_compound
                result["sentiment_label"] = "positive"
            elif vader_compound <= -0.05:
                result["sentiment_score"] = vader_compound
                result["sentiment_label"] = "negative"
            else:
                result["sentiment_score"] = 0.0
                result["sentiment_label"] = "neutral"
            result["sentiment_confidence"] = abs(vader_compound)
        
        # Transformer analysis (override if available)
        if self.transformer_available:
            try:
                transformer_result = self.transformer(text[:512])[0]
                label = transformer_result["label"].lower()
                score = transformer_result["score"]
                
                result["transformer"] = {
                    "label": label,
                    "score": score,
                }
                
                # Use transformer if more confident
                if score > result["sentiment_confidence"]:
                    result["sentiment_label"] = label
                    result["sentiment_confidence"] = score
                    if label == "positive":
                        result["sentiment_score"] = score
                    else:
                        result["sentiment_score"] = -score
            except Exception as e:
                print(f"Transformer error: {e}")
        
        # Aspect extraction
        if return_aspects and self.spacy_available:
            result["aspects"] = self.extract_aspects(text)
        
        # Emotion classification (simple rule-based)
        if return_emotions:
            result["emotions"] = self.classify_emotions(text)
        
        return result
    
    def extract_aspects(self, text: str) -> List[Dict]:
        """Extract aspects from text using spaCy"""
        aspects = []
        
        if not self.spacy_available:
            return aspects
        
        doc = self.nlp(text)
        
        # Extract noun chunks as potential aspects
        for chunk in doc.noun_chunks:
            # Simple sentiment for the aspect
            aspect_text = chunk.text.lower()
            
            # Check for opinion words nearby
            sentiment_words = {
                "positive": ["good", "great", "excellent", "amazing", "love", "best"],
                "negative": ["bad", "poor", "terrible", "worst", "hate", "awful"],
            }
            
            sentiment = "neutral"
            for token in chunk:
                if token.text.lower() in sentiment_words["positive"]:
                    sentiment = "positive"
                    break
                elif token.text.lower() in sentiment_words["negative"]:
                    sentiment = "negative"
                    break
            
            aspects.append({
                "aspect": chunk.text,
                "sentiment": sentiment,
                "span": [chunk.start, chunk.end],
            })
        
        return aspects[:10]  # Limit aspects
    
    def classify_emotions(self, text: str) -> List[Dict]:
        """Classify emotions in text (simple rule-based)"""
        text_lower = text.lower()
        
        emotions = {
            "joy": 0.0,
            "anger": 0.0,
            "sadness": 0.0,
            "fear": 0.0,
            "surprise": 0.0,
            "disgust": 0.0,
        }
        
        # Joy indicators
        joy_words = ["happy", "love", "great", "excellent", "amazing", "wonderful", "fantastic", "joy"]
        for word in joy_words:
            if word in text_lower:
                emotions["joy"] += 0.2
        
        # Anger indicators
        anger_words = ["angry", "hate", "furious", "annoyed", "irritated", "mad"]
        for word in anger_words:
            if word in text_lower:
                emotions["anger"] += 0.2
        
        # Sadness indicators
        sadness_words = ["sad", "disappointed", "unhappy", "upset", "depressed", "broken"]
        for word in sadness_words:
            if word in text_lower:
                emotions["sadness"] += 0.2
        
        # Fear indicators
        fear_words = ["scared", "afraid", "worried", "nervous", "fear", "terrified"]
        for word in fear_words:
            if word in text_lower:
                emotions["fear"] += 0.2
        
        # Surprise indicators
        surprise_words = ["surprised", "shocked", "amazing", "incredible", "unexpected"]
        for word in surprise_words:
            if word in text_lower:
                emotions["surprise"] += 0.2
        
        # Disgust indicators
        disgust_words = ["disgusting", "gross", "nasty", "sick", "repulsive"]
        for word in disgust_words:
            if word in text_lower:
                emotions["disgust"] += 0.2
        
        # Normalize to 0-1 range
        for emotion in emotions:
            emotions[emotion] = min(1.0, emotions[emotion])
        
        # Convert to list
        return [{"emotion": k, "score": v} for k, v in emotions.items() if v > 0]


class TopicModeler:
    """Topic modeling using BERTopic"""
    
    def __init__(self):
        self.model = None
        self.available = False
        
        try:
            from bertopic import BERTopic
            from sklearn.feature_extraction.text import CountVectorizer
            self.BERTopic = BERTopic
            self.available = True
        except ImportError:
            print("BERTopic not available")
    
    def fit(self, texts: List[str]) -> List[str]:
        """Fit topic model on texts"""
        if not self.available or not texts:
            return []
        
        try:
            # Simple topic modeling
            topics, probs = self.model.fit_transform(texts)
            return [f"Topic {t}" for t in topics]
        except Exception as e:
            print(f"Topic modeling error: {e}")
            return []
    
    def get_topics(self, texts: List[str], n_topics: int = 10) -> List[Dict]:
        """Get topic information"""
        if not self.available:
            return []
        
        try:
            topics, probs = self.model.fit_transform(texts)
            
            # Get topic info
            topic_info = self.model.get_topic_info()
            
            return [
                {
                    "topic_id": row["Topic"],
                    "count": row["Count"],
                    "representative": row["Representation"],
                }
                for _, row in topic_info.iterrows()
                if row["Topic"] >= 0
            ][:n_topics]
        except Exception as e:
            print(f"Topic info error: {e}")
            return []
