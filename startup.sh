#!/bin/sh
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn --workers 2 config.wsgi:application --bind 0.0.0.0:8000



