# Backend (Flask)

## Features
- `/health` health endpoint
- `/api/process-text` for pasted text
- `/api/process-pdf` for PDF/TXT upload (Docling for PDF)
- `/api/get-stats` for latest processing stats
- ORP and timing logic split into independent services
- Centralized error handling, upload limits, CORS, logging

## Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

## Test
```bash
cd backend
pytest -q
```

## Deploy (Render)
- Runtime command: `gunicorn app:app`
- Use `Procfile`
- Configure env vars from `.env.example`
