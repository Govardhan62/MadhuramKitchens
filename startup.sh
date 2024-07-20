#!/bin/sh

echo "Starting database migration..."
python manage.py migrate --noinput
if [ $? -ne 0 ]; then
    echo "Migration failed"
    exit 1
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput
if [ $? -ne 0 ]; then
    echo "Collectstatic failed"
    exit 1
fi

echo "Starting Gunicorn server..."
gunicorn --workers 2 config.wsgi:application --bind 0.0.0.0:8000
if [ $? -ne 0 ]; then
    echo "Gunicorn failed to start"
    exit 1
fi
