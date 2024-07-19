#!/bin/bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn --workers 2 config.wsgi
