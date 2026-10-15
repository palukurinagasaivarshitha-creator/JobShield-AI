import os
import logging
from typing import Dict, Any, Tuple
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from app.core.config import settings

logger = logging.getLogger(__name__)

# Global model cache to avoid repeated disk I/O on every request
_CACHED_MODEL = None


def build_pipeline() -> Pipeline:
    """
    Constructs an end-to-end NLP classification pipeline:
    1. TfidfVectorizer: N-grams (unigram + bigram), sublinear term frequency scaling, stopword filtering.
    2. LogisticRegression: Balanced class weighting to handle recruitment fraud imbalance (~5% fraud rate).
    """
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        stop_words="english",
        sublinear_tf=True
    )
    classifier = LogisticRegression(
        class_weight="balanced",
        C=1.0,
        max_iter=1000,
        random_state=42
    )
    return Pipeline([
        ("tfidf", vectorizer),
        ("clf", classifier)
    ])


def load_trained_model(model_path: str = None) -> Pipeline | None:
    """
    Loads saved model artifact from disk or returns None if not yet trained.
    """
    global _CACHED_MODEL
    if _CACHED_MODEL is not None:
        return _CACHED_MODEL

    path = model_path or settings.MODEL_PATH
    if os.path.exists(path) and os.path.getsize(path) > 0:
        try:
            logger.info(f"Loading trained model artifact from {path}")
            _CACHED_MODEL = joblib.load(path)
            return _CACHED_MODEL
        except Exception as e:
            logger.error(f"Failed to load trained model from {path}: {e}")
            return None
    return None


def fallback_predict(text: str) -> Dict[str, Any]:
    """
    Deterministic heuristic fallback analysis mode used when model artifact is unavailable.
    Explicitly flags is_fallback: True to maintain scientific and regulatory transparency.
    """
    lower = text.lower()
    scam_keywords = [
        "telegram", "registration fee", "western union", "cashier's check",
        "bitcoin", "crypto", "wire transfer", "deposit a check", "mystery shopper",
        "package forwarding", "no interview", "start working today", "zelle", "cashapp"
    ]
    matched = [kw for kw in scam_keywords if kw in lower]
    fraud_score = min(len(matched) * 0.35, 0.95) if matched else 0.08
    is_fake = fraud_score >= 0.50
    confidence = round(fraud_score if is_fake else (1.0 - fraud_score), 3)

    return {
        "is_fake": is_fake,
        "confidence": confidence,
        "fraud_probability": round(fraud_score, 3),
        "risk_score": round(fraud_score * 100.0, 1),
        "features_analyzed": ["deterministic_keyword_density", "text_heuristic_scan"],
        "is_fallback": True,
        "algorithm": "Heuristic Rule Fallback (Model uninitialized)"
    }


def predict_job(title: str, description: str, company: str = "", requirements: str = "") -> Dict[str, Any]:
    """
    Performs inference using the trained ML model, or gracefully falls back to deterministic analysis.
    """
    corpus_text = f"{title or ''} {company or ''} {description or ''} {requirements or ''}".strip()
    model = load_trained_model()

    if model is None:
        return fallback_predict(corpus_text)

    try:
        # LogisticRegression predict_proba gives [prob_legitimate, prob_fraudulent]
        probabilities = model.predict_proba([corpus_text])[0]
        prob_fraud = float(probabilities[1])
        is_fake = prob_fraud >= 0.50
        confidence = float(probabilities[1] if is_fake else probabilities[0])

        return {
            "is_fake": is_fake,
            "confidence": round(confidence, 3),
            "fraud_probability": round(prob_fraud, 3),
            "risk_score": round(prob_fraud * 100.0, 1),
            "features_analyzed": ["job_title", "company_profile", "description", "requirements"],
            "is_fallback": False,
            "algorithm": "TF-IDF + Calibrated Logistic Regression (EMSCAD trained)"
        }
    except Exception as e:
        logger.error(f"Model inference failed with exception: {e}. Activating deterministic fallback.")
        return fallback_predict(corpus_text)
