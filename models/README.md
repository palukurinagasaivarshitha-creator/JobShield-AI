# Fake Job Detection Machine Learning Models

## Model Overview
This directory contains serialized machine learning pipelines trained on the Employment Scam Aegean Dataset (EMSCAD).

## Pipeline Architecture
1. **Feature Extraction**:
   - `TfidfVectorizer`: Unigrams and bigrams (`ngram_range=(1, 2)`), English stop-words removed, `sublinear_tf=True`, `max_features=5000`.
   - Concatenated text inputs: `title` + `company_profile` + `description` + `requirements`.
2. **Classifier**:
   - Calibrated Logistic Regression with balanced class weights / Random Forest ensemble.
   - Outputs calibrated probabilities between 0.0 and 1.0.
3. **Artifacts**:
   - `fake_job_detector.joblib`: Complete fitted `sklearn.pipeline.Pipeline` containing vectorizer + classifier.
   - `evaluation_report.json`: Metrics across train/test splits including accuracy, precision, recall, F1-score, and confusion matrix.

## Fallback Mechanism
If `fake_job_detector.joblib` is not yet generated or missing, the backend seamlessly activates its deterministic heuristic analysis engine, labeling all outputs with `is_fallback: true` to maintain transparent integrity.

## Training Instructions
To train or retrain the model:
```bash
python -m app.ml.train
```
To evaluate the model:
```bash
python -m app.ml.evaluate
```
