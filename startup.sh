#!/bin/bash

# Export environment variables
export DJANGO_SETTINGS_MODULE=config.settings

#install dependencies
pip install -r requirements.txt

python manage.py migrate

python manage.py collectstatic --noinput

gunicorn --workers 2 config.wsgi:application
