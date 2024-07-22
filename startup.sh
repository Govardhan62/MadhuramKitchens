#!/bin/sh

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python -m venv venv
fi

# Activate the virtual environment
. venv/bin/activate

# Ensure the Python environment is set up correctly
pip install --upgrade pip
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start the application using gunicorn
gunicorn --workers 4 config.wsgi:application --bind 0.0.0.0:443
