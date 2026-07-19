# Deployment Guide

## Overview

This project runs as a FastAPI backend with a PostgreSQL database. The React admin portal is **admin only** -- pilgrims never log into the React app; they use the Flutter mobile app (not yet built).

**Backend default port:** 8000

---

## Docker Deployment (Development)

### Quick Start

```bash
docker compose up --build
```

This starts:
- PostgreSQL on port 5432
- FastAPI backend on port 8000
- Auto-runs Alembic migrations on startup

The development container mounts the backend source code for live reload.

### Production Mode

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

Production differences:
- No source code volume mount (images are self-contained)
- Uses Gunicorn with Uvicorn workers (default 2 workers)
- Named volumes for database data and audio cache
- Health checks enabled
- Requires a `.env` file with production secrets

---

## Render Deployment

### Automatic (render.yaml)

The `render.yaml` file defines the full infrastructure as code. When you connect your repository to Render:

1. Render reads `render.yaml` and provisions:
   - A **Web Service** (Python, Starter plan) for the backend API
   - A **PostgreSQL** database (Starter plan)

2. The build pipeline:
   ```
   cd backend
   pip install -r requirements.txt
   alembic upgrade head
   ```

3. The start command:
   ```
   cd backend
   gunicorn app.main:app \
     --workers 2 \
     --worker-class uvicorn.workers.UvicornWorker \
     --bind 0.0.0.0:$PORT \
     --timeout 120 \
     --graceful-timeout 30 \
     --access-logfile - \
     --error-logfile -
   ```

4. Health check path: `/api/v1/health`
5. Auto-deploy is enabled on every push.
6. A 1GB persistent disk is mounted at `/app/audio_cache` for TTS audio files.

### Manual Setup

If you prefer to set up Render manually without `render.yaml`:

1. **Create a PostgreSQL database:**
   - Go to Render Dashboard > New > PostgreSQL
   - Note the internal connection string (format: `postgresql://user:password@host:5432/dbname`)
   - Add the connection string as `DATABASE_URL` environment variable on the web service

2. **Create a Web Service:**
   - Go to Render Dashboard > New > Web Service
   - Connect your GitHub repository
   - Runtime: Python
   - Build command:
     ```
     cd backend && pip install -r requirements.txt && alembic upgrade head
     ```
   - Start command:
     ```
     cd backend && gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --timeout 120 --graceful-timeout 30 --access-logfile - --error-logfile -
     ```
   - Health check path: `/api/v1/health`

3. **Create a disk (optional but recommended):**
   - Type: Persistent Disk
   - Mount path: `/app/audio_cache`
   - Size: 1GB

---

## Environment Variables

All environment variables are defined in `backend/.env.example`. Copy this file to `backend/.env` for local development.

| Variable                | Required | Default | Description                                                                 |
|-------------------------|----------|---------|-----------------------------------------------------------------------------|
| `DATABASE_URL`          | Yes      | --      | PostgreSQL connection string. Format: `postgresql://user:password@host:5432/dbname` |
| `SECRET_KEY`            | Yes      | --      | JWT signing key. Generate with: `python -c "import secrets; print(secrets.token_hex(32))"` |
| `DEBUG`                 | No       | `False` | Enable debug mode. Set to `False` in production.                            |
| `APP_VERSION`           | No       | `1.0.0` | Application version string.                                                 |
| `CORS_ORIGINS`          | No       | `["http://localhost:5173"]` | Allowed CORS origins. JSON array of strings.                       |
| `GEMINI_API_KEY`        | No       | `""`    | Google Gemini API key for AI personalization features.                       |
| `FIREBASE_CREDENTIALS_PATH` | No   | `""`    | Path to Firebase service account JSON for FCM push notifications.           |
| `HOST`                  | No       | `0.0.0.0` | Server bind address.                                                     |
| `PORT`                  | No       | `8000`  | Server port.                                                               |
| `WORKERS`               | No       | `2`     | Number of Gunicorn workers.                                                |

### CORS Origins Format

The `CORS_ORIGINS` variable is a JSON array string:

```bash
# Local development
CORS_ORIGINS=["http://localhost:5173"]

# Production
CORS_ORIGINS=["https://your-admin-domain.onrender.com"]

# Multiple origins
CORS_ORIGINS=["https://admin.hajj.ng", "https://www.hajj.ng"]
```

### Firebase Configuration

For push notifications (Flutter app), set `FIREBASE_CREDENTIALS_PATH` to the path of your Firebase service account JSON file. This is optional -- the system works without it but push notifications will be unavailable.

---

## Database Migration on Deploy

Migrations are handled by Alembic and run automatically on container startup.

### How It Works

The `entrypoint.sh` script runs before the application starts:

```bash
#!/bin/sh
set -e
echo "Running Alembic migrations..."
alembic upgrade head
echo "Starting application..."
exec gunicorn app.main:app ...
```

### Manual Migration

If you need to run migrations manually:

```bash
# Local development
cd backend
alembic upgrade head

# Docker
docker exec hajj_api_dev alembic upgrade head

# Create a new migration after model changes
alembic revision --autogenerate -m "description of changes"
```

### Migration Files

Migration files are in `backend/alembic/versions/`. They are version-controlled and applied in order by Alembic.

---

## Post-Deployment Verification

After deployment, verify everything is working:

### 1. Health Check

```bash
curl https://your-domain.com/api/v1/health
```

Expected response:
```json
{
  "success": true,
  "message": "Service is healthy",
  "data": {"status": "healthy"},
  "errors": null
}
```

### 2. Login

```bash
curl -X POST https://your-domain.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@hajj.ng", "password": "admin123"}'
```

Expected response:
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ..."
  },
  "errors": null
}
```

### 3. Dashboard Stats

```bash
curl https://your-domain.com/api/v1/stats \
  -H "Authorization: Bearer <access_token>"
```

Expected response:
```json
{
  "success": true,
  "message": "Dashboard statistics retrieved successfully",
  "data": {
    "total_pilgrims": 0,
    "active_pilgrims": 0,
    "total_packages": 0,
    "total_flights": 0,
    "total_accommodations": 0,
    "total_transports": 0,
    "total_announcements": 0,
    "total_notifications": 0,
    "total_preferences": 0
  },
  "errors": null
}
```

### 4. Swagger UI

Navigate to `https://your-domain.com/docs` to verify the interactive API documentation loads.

### 5. Admin Portal

If the React admin portal is deployed, verify it can connect to the backend by logging in with the admin credentials.

### 6. Database Migrations

Check that migrations ran successfully by querying the database or checking application logs for any migration errors on startup.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `DATABASE_URL` connection refused | Ensure PostgreSQL is running and the connection string is correct. Check Render database credentials. |
| `SECRET_KEY` warning | The key is weak or default. Generate a strong key: `python -c "import secrets; print(secrets.token_hex(32))"` |
| CORS errors | Add your admin portal domain to `CORS_ORIGINS`. |
| AI endpoints return 503 | Set `GEMINI_API_KEY` environment variable. AI features are optional. |
| Push notifications not working | Set `FIREBASE_CREDENTIALS_PATH` to a valid Firebase service account JSON. |
| Port already in use | Change `PORT` environment variable or stop the conflicting service. |
