#!/bin/sh
set -e

python -c "from app import ensure_images; ensure_images()"

exec gunicorn \
    --workers "${GUNICORN_WORKERS:-4}" \
    --bind 0.0.0.0:5023 \
    --access-logfile - \
    --error-logfile - \
    app:app
