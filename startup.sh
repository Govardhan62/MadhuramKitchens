#!/bin/sh
python manage.py migrate && python manage.py collectstatic && gunicorn --workers 2 config.wsgi --bind 0.0.0.0:8000


