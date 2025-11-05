#!/usr/bin/env bash
set -e

# Start the FastAPI app with Gunicorn + Uvicorn worker, binding to Railway's $PORT
exec gunicorn backend.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8000}
