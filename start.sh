#!/usr/bin/env bash
# Render start script for Fashion Store

echo "🚀 Starting Fashion Store on Render..."

# Start Gunicorn server
exec gunicorn fashion_store.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --worker-class gthread \
    --worker-connections 1000 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 30 \
    --keep-alive 2 \
    --log-level info \
    --access-logfile - \
    --error-logfile - \
    --env DJANGO_SETTINGS_MODULE=fashion_store.production_settings