#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Ensure the Python environment is set up correctly
python -m pip install --upgrade pip
pip install -r requirements.txt

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the application using Gunicorn
echo "Starting the application..."
gunicorn --workers 4 config.wsgi:application --bind 0.0.0.0:443
