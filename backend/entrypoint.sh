#!/bin/sh
set -e

echo "Running Alembic migrations..."
alembic upgrade head

echo "Seeding admin user..."
python seed.py

echo "Seeding sample data..."
python seed_data.py || true

echo "Starting application..."
exec gunicorn app.main:app \
  --workers "${WORKERS:-2}" \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind "${HOST:-0.0.0.0}:${PORT:-8000}" \
  --timeout 120 \
  --graceful-timeout 30 \
  --access-logfile - \
  --error-logfile - \
  --log-level "${LOG_LEVEL:-info}"
