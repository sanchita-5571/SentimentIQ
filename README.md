# SentimentIQ

SentimentIQ is a local-only full-stack application for ingesting customer reviews, scoring sentiment, extracting aspects and topics, and diagnosing the earliest drivers behind sentiment drops.

## Stack

- Frontend: React, Tailwind CSS, Zustand, Recharts
- Backend: FastAPI, SQLAlchemy
- Data: MongoDB for review/event documents, Redis for cache, SQLAlchemy-backed SQLite for local auth and export metadata
- NLP: VADER, Transformers, BERTopic with keyword fallbacks

## What It Does

- Review ingestion from CSV, JSON, and manual input
- NLP pipeline for cleaning, deduplication, language detection, sentiment scoring, aspect extraction, and topic extraction
- Root cause engine for sentiment-drop detection, earliest degrading aspect detection, amplification chain tracing, and recommendations
- Dashboard with overview, trend analytics, drilldown, verbatims explorer, and report export
- Local auth, loading states, error boundaries, cached reads, persisted filters, and live chart refresh

## Project Structure

```text
backend/
  api/v1/             FastAPI routes
  core/               config and security
  db/                 MongoDB, Redis, SQLAlchemy setup
  services/           ingestion, NLP, dashboard, root-cause logic
  schemas/            API request/response contracts
  seed.py             sample data loader
frontend/
  src/pages/          dashboard screens
  src/components/     layout and UI blocks
  src/stores/         Zustand stores
  src/api/            API client
sample_data/
  reviews_sample.csv
  reviews_sample.json
```

## Local Requirements

- Python 3.10+
- Node.js 18+
- MongoDB running on `localhost:27017`
- Redis running on `localhost:6379`

No deployment configs, cloud services, or paid APIs are required.

## Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `backend/.env` from the repo root `.env.example` or copy the values manually.

Run the API:

```bash
uvicorn main:app --reload
```

Seed local demo data:

```bash
python seed.py
```

The API will be available at [http://localhost:8000](http://localhost:8000) and docs at [http://localhost:8000/docs](http://localhost:8000/docs).

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at [http://localhost:5173](http://localhost:5173).

## Demo Login

- `analyst@example.com` / `demo123`
- `admin@example.com` / `admin123`

These users are created automatically in the local SQLAlchemy store at startup.

## API Overview

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `GET /api/v1/dashboard/snapshot`
- `GET /api/v1/reviews`
- `POST /api/v1/reviews/manual`
- `POST /api/v1/reviews/upload/csv`
- `POST /api/v1/reviews/upload/json`
- `GET /api/v1/root-causes`
- `POST /api/v1/root-causes/rebuild`
- `POST /api/v1/reports/export`

## Sample Data Notes

- `reviews_sample.csv` contains dated review history that is useful for trend and root-cause detection.
- `reviews_sample.json` contains extra dated verbatims to enrich topic and aspect coverage.

## Local Data Model

- MongoDB collections: reviews, events, ingestion_batches, report_exports
- SQLAlchemy tables: users, ingestion_batches, report_exports
- Redis keys: dashboard snapshots and root-cause cache entries

## Known Behavior

- Transformers load lazily and only enrich English sentiment when available.
- BERTopic is attempted on larger batches; if it fails or the batch is small, keyword topic extraction is used instead.
- Root-cause events depend on dated reviews. If all reviews share the same timestamp, the drilldown will remain sparse.
