#!/bin/bash
# Export environment variables
python manage.py collectstatic --noinput && gunicorn --workers 2 config.wsgi
