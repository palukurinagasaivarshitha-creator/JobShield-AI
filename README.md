# Fake Job Detection & Verification Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3-61dafb.svg)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.4-646cff.svg)](https://vitejs.dev/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.4%2B-f7931e.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An enterprise-grade, multi-vector cybersecurity intelligence platform engineered to protect job seekers from recruitment fraud, advance fee scams, lookalike phishing portals, and employer impersonation.

Powered by the **Employment Scam Aegean Dataset (EMSCAD)**, deterministic heuristic pattern recognition, authoritative DNS corroboration, and an interactive React dashboard.

---

## Table of Contents

1. [Key Features](#key-features)
2. [Architecture Overview](#architecture-overview)
3. [Prerequisites](#prerequisites)
4. [Quick Start (Windows Automated)](#quick-start-windows-automated)
5. [Manual Installation & Setup](#manual-installation--setup)
   - [Backend Setup](#1-backend-setup)
   - [Machine Learning Training](#2-machine-learning-training)
   - [Frontend Setup](#3-frontend-setup)
6. [Database Configuration (PostgreSQL & SQLite)](#database-configuration)
7. [Official Apply Corroboration Engine](#official-apply-corroboration-engine)
8. [Running Tests](#running-tests)
9. [Docker Deployment](#docker-deployment)
10. [REST API Documentation](#rest-api-documentation)
11. [Troubleshooting Guide](#troubleshooting-guide)
12. [Dataset Citation & Licence](#dataset-citation--licence)

---

## Key Features

- **Dual-Vector Analysis Engine**: Combines statistical NLP machine learning (TF-IDF + Calibrated Logistic Regression) with a deterministic pattern-matching engine (detecting wire transfers, Telegram interviews, counterfeit checks, upfront fees).
- **Official Company Website & Apply Feature**: Corroborates submitted job postings against authoritative DNS records, enterprise registries (Google, Amazon, Microsoft, Netflix, etc.), and verified Applicant Tracking Systems (ATS). If verified, provides an **"Apply on Official Website"** link. If domain spoofing is detected, raises a **CRITICAL Domain Mismatch** alert.
- **SSRF Protection & URL Guards**: Ingests external job links safely by blocking loopback (`127.0.0.0/8`), private networks (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), and cloud metadata (`169.254.169.254`).
- **Interactive Security Dashboard**: Real-time telemetry, threat metrics, and chronological audit logs with searchable and filterable database storage.
- **Pure JavaScript/JSX Frontend**: Built with React and Vite without any TypeScript complexity.
- **Plug-and-Play Offline Readiness**: Includes a validated seed dataset with verified recruitment fraud signatures so the platform functions immediately without external network dependencies.

---

## Architecture Overview

```
FakeJobDetection/
├── frontend/                     # React + Vite UI (JavaScript & JSX only)
│   ├── src/
│   │   ├── components/           # Reusable UI components (RiskGauge, RiskBadge, JobCard)
│   │   ├── pages/                # Landing, Dashboard, Analyze, Detail, Search, History
│   │   ├── services/             # API client service
│   │   ├── styles/               # Modern dark/light cyber-defense design system
│   │   ├── App.jsx               # Application routing coordinator
│   │   └── main.jsx              # React DOM entrypoint
│   ├── package.json
│   └── vite.config.js
├── backend/                      # Python 3 + FastAPI REST API
│   ├── app/
│   │   ├── api/routes/           # Endpoints: analyze, verify, jobs, history, health
│   │   ├── core/                 # Configuration and environment settings
│   │   ├── database/             # SQLAlchemy engine & SQLite/Postgres sessions
│   │   ├── models/               # ORM models (JobAnalysis, JobSearchListing)
│   │   ├── schemas/              # Pydantic v2 validation models
│   │   ├── services/             # Scraper (SSRF guard), rule_engine, domain_verifier
│   │   ├── ml/                   # EMSCAD dataset loader, pipeline, train, evaluate
│   │   └── main.py               # FastAPI application entrypoint
│   ├── tests/                    # 17 automated Pytest test suites
│   ├── requirements.txt
│   └── .env.example
├── data/                         # EMSCAD dataset & validated seed corpus
│   ├── seed_jobs.csv             # Bundled representative dataset
│   └── README.md                 # Dataset documentation and column schema
├── models/                       # Trained machine learning artifacts
│   ├── fake_job_detector.joblib  # Serialized Scikit-learn pipeline
│   ├── evaluation_report.json    # Accuracy, Precision, Recall, F1, Confusion Matrix
│   └── README.md
├── docs/                         # Architecture diagrams & REST API reference
│   ├── architecture.md
│   └── API.md
├── scripts/                      # Windows automation & project export scripts
│   ├── setup.bat                 # One-click Windows setup
│   ├── run.bat                   # One-click dual server launcher
│   └── export_project.py         # ZIP archive exporter
├── docker-compose.yml            # Multi-container PostgreSQL + FastAPI stack
├── Dockerfile                    # Container definition for backend
├── README.md
└── LICENSE                       # MIT License
```

---

## Prerequisites

- **Python**: Version 3.10, 3.11, 3.12, 3.13, or 3.14
- **Node.js**: Version 18.x or newer (includes `npm`)
- **Git** (Optional, for version control)
- **PostgreSQL** (Optional, for production deployments; SQLite is enabled by default for zero-config local development)

---

## Quick Start (Windows Automated)

Two automated batch scripts are provided in the `scripts/` folder:

1. **One-Click Setup**:
   ```cmd
   scripts\setup.bat
   ```
   *Checks Python and Node.js runtimes, creates a virtual environment, installs Python and Node dependencies, and trains the machine learning baseline model.*

2. **One-Click Launch**:
   ```cmd
   scripts\run.bat
   ```
   *Launches the FastAPI backend on `http://localhost:8000` and Vite frontend on `http://localhost:5173` in two separate terminal windows.*

---

## Manual Installation & Setup

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate Python virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt

# Create environment configuration
copy .env.example .env
```

### 2. Machine Learning Training

The platform trains a baseline TF-IDF + Calibrated Logistic Regression pipeline using stratified cross-validation:

```bash
# Run training pipeline (saves model to models/fake_job_detector.joblib)
python -m app.ml.train

# Inspect performance evaluation metrics
python -m app.ml.evaluate
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install npm dependencies
npm install

# Start Vite development server
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## Database Configuration

The application uses SQLAlchemy ORM and supports both SQLite and PostgreSQL.

### Option A: Local Development (SQLite - Zero Config)
In `backend/.env`:
```ini
DATABASE_URL=sqlite:///./fake_jobs.db
```
*No database installation is required; tables are created automatically on startup.*

### Option B: Production (PostgreSQL)
Install PostgreSQL and create a database named `fakejobdb`:
```sql
CREATE DATABASE fakejobdb;
```
Update `backend/.env`:
```ini
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/fakejobdb
```

---

## Official Apply Corroboration Engine

A core differentiator of this platform is the **Official Company Website and Apply Feature**:

1. **URL Validation**: Analyzes submitted job URLs and checks for SSRF threats, link-shorteners, and suspicious TLDs (`.xyz`, `.top`, `.work`).
2. **Enterprise Registry Corroboration**: Compares claimed companies against verified corporate domains (Google, Amazon, Microsoft, Netflix, Apple, Meta, etc.).
3. **Vacancy Corroboration**:
   - If the job posting is directly hosted on the official employer's domain or their verified ATS tenant (e.g., `boards.greenhouse.io`, `jobs.lever.co`, `careers.google.com`), an **"Apply on Official Website"** button is rendered.
   - If the company is genuine but the specific link was on a third-party site, the system provides a link to the verified corporate careers portal with a caution note.
   - If domain spoofing is detected (e.g. claiming Google but hosted on `google-career-portal.xyz`), a **Domain Mismatch Warning** is raised and application links are blocked.

---

## Running Tests

Automated testing is implemented using Pytest:

```bash
cd backend
pytest -v
```

Tests cover:
- Health check and root endpoints
- Legitimate job analysis with official domain match
- Fraudulent scam job detection (fees, wire fraud, Telegram)
- Impersonation and lookalike domain phishing detection
- SSRF network guards (blocking localhost, private IPs, loopbacks)
- Pydantic input validation and empty field handling
- Search and analytics telemetry endpoints

To verify the frontend build:
```bash
cd frontend
npm run build
```

---

## Docker Deployment

To launch the full production stack using Docker Compose:

```bash
docker-compose up --build -d
```

This starts:
- **PostgreSQL 15 Container**: Listening on port `5432`
- **FastAPI Backend Container**: Listening on port `8000`

---

## REST API Documentation

FastAPI provides interactive API documentation out of the box:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

Key Endpoints:
- `POST /api/analyze` - Evaluates job posting authenticity and returns composite threat report.
- `POST /api/extract` - Safely extracts title, company, and description from a URL.
- `POST /api/verify` - Verifies company domain registration and vacancy links.
- `GET /api/jobs/search` - Searches cataloged genuine and scam job listings.
- `GET /api/jobs/dashboard/stats` - Returns aggregate threat telemetry.
- `GET /api/history` - Queries chronological scan audit logs.

For complete payload examples, see [docs/API.md](docs/API.md).

---

## Troubleshooting Guide

| Issue | Cause | Resolution |
|---|---|---|
| `SSRF Guard: Resolved IP belongs to private network` | URL resolves to localhost or private subnet | Provide a public, valid HTTP/HTTPS URL. Local and internal addresses are blocked for security. |
| `Pydantic validation error: Either a valid job_url or non-empty description` | Both URL and Description were empty | Provide at least a job posting URL or paste the job description text. |
| `Deterministic fallback mode active` | ML model artifact `.joblib` not found | Run `python -m app.ml.train` inside `backend/` to generate the model. |
| `Database connection error` | PostgreSQL server unreachable | Check credentials in `.env` or leave `DATABASE_URL=sqlite:///./fake_jobs.db` for automatic SQLite fallback. |

---

## Dataset Citation & Licence

The machine learning models in this repository are based on research from the University of the Aegean:

> **Vidros, S., Kolias, C., Kambourakis, G., & Akoglu, L. (2017).**  
> *Automatic Detection of Online Recruitment Frauds: Characteristics, Methods, and a Public Dataset.*  
> Future Internet, 9(1), 6. [DOI: 10.3390/fi9010006](https://doi.org/10.3390/fi9010006)

Released under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** licence.
Project source code is licensed under the [MIT License](LICENSE).
