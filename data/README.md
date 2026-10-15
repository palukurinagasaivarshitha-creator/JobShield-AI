# EMSCAD Dataset Documentation & Setup

## 1. Dataset Overview

This project utilizes the **Employment Scam Aegean Dataset (EMSCAD)**, originally published by the University of the Aegean Laboratory of Information & Communication Systems Security (ICCS).

- **Official Source**: [University of the Aegean EMSCAD Repository](http://recruiting.icsd.aegean.gr/scamdata/) / Kaggle Mirror ([Real / Fake Job Posting Prediction](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction)).
- **Citation**: S. Vidros, C. Kolias, G. Kambourakis, L. Akoglu, "Automatic Detection of Online Recruitment Frauds: Characteristics, Methods, and a Public Dataset", Future Internet 2017, 9(1), 6; DOI: 10.3390/fi9010006.
- **Licence**: Creative Commons Attribution 4.0 International (CC BY 4.0).
- **Scope**: 17,880 real-life job advertisements posted between 2012 and 2014, with ground-truth verification.
- **Class Distribution**:
  - Real Job Postings: 17,014 (~95.16%)
  - Fraudulent Postings: 866 (~4.84%)
  - Imbalanced binary classification problem.

## 2. Feature Schema & Column Definitions

| Column Name | Type | Description |
|---|---|---|
| `job_id` | Integer | Unique identifier for each posting |
| `title` | Text | Title of the position offered |
| `location` | Text | Geographic location (Country, State, City) |
| `department` | Text | Corporate department offering the role |
| `salary_range` | Text | Stated compensation range (e.g., "50000-75000") |
| `company_profile` | Text | Overview of the recruiting company |
| `description` | Text | Detailed explanation of job responsibilities |
| `requirements` | Text | Qualifications, skills, and prerequisite experience |
| `benefits` | Text | Perquisites offered by the employer |
| `telecommuting` | Binary | 1 if remote work allowed; 0 otherwise |
| `has_company_logo` | Binary | 1 if company logo was present; 0 otherwise |
| `has_questions` | Binary | 1 if application includes screening questions |
| `employment_type` | Text | Full-time, Part-time, Contract, Temporary, Other |
| `required_experience`| Text | Internship, Entry level, Associate, Mid-Senior, Executive |
| `required_education` | Text | High School, Bachelor's, Master's, Unspecified |
| `industry` | Text | Sector (e.g., Computer Software, Oil & Energy, Healthcare) |
| `function` | Text | Departmental role (e.g., Engineering, Sales, Customer Service) |
| `fraudulent` | Binary | **Target Variable**: 1 = Scam / Fake Job; 0 = Legitimate Job |

## 3. Preprocessing, Cleaning & Leakage Prevention

1. **Text Combination**:
   To represent the textual reality of job postings accurately, `title`, `company_profile`, `description`, and `requirements` are concatenated into a consolidated corpus string.
2. **Missing Value Imputation**:
   Empty text fields are imputed with empty strings to reflect real-world scenarios where fraudulent postings omit company profiles or detailed requirements.
3. **Leakage Prevention**:
   The TF-IDF vectorizer is fitted **strictly on the training split** after stratified 80/20 train/test partitioning. The test split is never observed during vocabulary construction or parameter estimation.
4. **Class Imbalance Strategy**:
   Class weighting (`balanced`) is utilized in the classifier to account for the ~5% minority fraud prevalence, penalizing false negatives proportionally.

## 4. How to Download the Full Dataset

Run the automated download/import script:
```bash
cd backend
python -m app.ml.dataset_loader
```
Or manually place the official `fake_job_postings.csv` into `data/emscad_dataset.csv`.

## 5. Seed Dataset for Autonomous Out-of-the-Box Operation

For immediate offline demonstration, college project review, and unit tests when external internet downloads may be blocked by firewalls, this repository bundles a representative seed corpus (`seed_jobs.csv`) derived directly from verified EMSCAD patterns and real recruitment fraud signatures.
