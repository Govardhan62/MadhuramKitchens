#!/bin/bash

# Exit on any error
set -e

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the Gunicorn server
echo "Starting Gunicorn server..."
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT