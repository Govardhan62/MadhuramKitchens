#!/bin/sh
python manage.py migrate && python manage.py collectstatic && gunicorn --workers 2 config.wsgi:application --bind 0.0.0.0:8000