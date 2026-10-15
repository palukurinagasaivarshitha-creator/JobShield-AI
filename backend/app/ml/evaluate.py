import json
import logging
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import joblib
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from app.core.config import settings
from app.ml.dataset_loader import load_dataset

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ml_evaluate")

def run_evaluation(model_path: str = None, dataset_path: str = None) -> dict:
    target_model_path = model_path or settings.MODEL_PATH
    if not os.path.exists(target_model_path):
        logger.warning(f"No trained model found at {target_model_path}. Please run train.py first.")
        return {"status": "error", "message": f"Model artifact not found at {target_model_path}"}

    model = joblib.load(target_model_path)
    df = load_dataset(dataset_path)

    X = df["combined_text"]
    y = df["fraudulent"]

    y_pred = model.predict(X)
    y_proba = model.predict_proba(X)[:, 1]

    acc = float(accuracy_score(y, y_pred))
    prec = float(precision_score(y, y_pred, zero_division=0))
    rec = float(recall_score(y, y_pred, zero_division=0))
    f1 = float(f1_score(y, y_pred, zero_division=0))
    cm = confusion_matrix(y, y_pred).tolist()
    report_text = classification_report(y, y_pred, target_names=["Legitimate", "Fraudulent"])

    results = {
        "status": "success",
        "sample_count": len(df),
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "confusion_matrix": cm,
        "classification_report": report_text
    }
    return results

if __name__ == "__main__":
    res = run_evaluation()
    if res.get("status") == "success":
        print("\n" + "=" * 60)
        print("MODEL PERFORMANCE EVALUATION")
        print("=" * 60)
        print(f"Evaluated on {res['sample_count']} samples:")
        print(f"Accuracy:  {res['accuracy']:.4f}")
        print(f"Precision: {res['precision']:.4f}")
        print(f"Recall:    {res['recall']:.4f}")
        print(f"F1 Score:  {res['f1_score']:.4f}")
        print("\nClassification Report:\n" + res["classification_report"])
        print("=" * 60)
    else:
        print(res.get("message"))
