#!/usr/bin/env bash
set -e

# Start the FastAPI app with Uvicorn, binding to Railway's $PORT (or 8000 default)
exec uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000} --proxy-headers
