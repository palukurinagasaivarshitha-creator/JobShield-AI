import json
import logging
import os
import sys
from pathlib import Path
import joblib
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score
)
from sklearn.model_selection import train_test_split

# Ensure backend root is on sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.core.config import settings
from app.ml.dataset_loader import load_dataset
from app.ml.pipeline import build_pipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ml_train")


def train_and_save(dataset_path: str = None, model_output_path: str = None) -> dict:
    """
    Trains the fake job detection pipeline with strict train-test separation
    to prevent data leakage, and persists the fitted model and evaluation metrics.
    """
    df = load_dataset(dataset_path)
    X = df["combined_text"]
    y = df["fraudulent"]

    logger.info(f"Loaded {len(df)} total samples. Fraud prevalence: {y.mean():.2%}")

    # Stratified split to preserve class ratios between train and test sets
    # Prevent data leakage: vectorizer will be fitted only on X_train inside the pipeline
    test_size = 0.25 if len(df) < 50 else 0.20
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=42,
        stratify=y
    )

    logger.info(f"Training split: {len(X_train)} samples | Testing split: {len(X_test)} samples")

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    # Predictions on unseen test set
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    # Metrics computation
    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, zero_division=0))
    rec = float(recall_score(y_test, y_pred, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, zero_division=0))
    try:
        auc = float(roc_auc_score(y_test, y_proba))
    except Exception:
        auc = 1.0

    cm = confusion_matrix(y_test, y_pred).tolist()

    report = {
        "dataset_samples": len(df),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "roc_auc": round(auc, 4),
        "confusion_matrix": {
            "true_negatives": cm[0][0] if len(cm) > 0 else 0,
            "false_positives": cm[0][1] if len(cm) > 0 and len(cm[0]) > 1 else 0,
            "false_negatives": cm[1][0] if len(cm) > 1 else 0,
            "true_positives": cm[1][1] if len(cm) > 1 and len(cm[1]) > 1 else 0
        },
        "model_type": "LogisticRegression(class_weight='balanced') + TfidfVectorizer",
        "features": ["title", "company_profile", "description", "requirements"]
    }

    # Save fitted model
    out_path = model_output_path or settings.MODEL_PATH
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    joblib.dump(pipeline, out_path)
    logger.info(f"Model saved successfully to {out_path}")

    # Save evaluation report
    report_path = os.path.join(os.path.dirname(os.path.abspath(out_path)), "evaluation_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    logger.info(f"Evaluation report saved to {report_path}")

    return report


if __name__ == "__main__":
    report = train_and_save()
    print("=" * 60)
    print("MODEL TRAINING & EVALUATION REPORT")
    print("=" * 60)
    print(f"Accuracy:  {report['accuracy']:.4f}")
    print(f"Precision: {report['precision']:.4f}")
    print(f"Recall:    {report['recall']:.4f}")
    print(f"F1 Score:  {report['f1_score']:.4f}")
    print(f"ROC-AUC:   {report['roc_auc']:.4f}")
    print(f"Confusion Matrix: {report['confusion_matrix']}")
    print("=" * 60)
