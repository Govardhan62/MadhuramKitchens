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

# Start the application using gunicorn
<<<<<<< HEAD
echo "Starting the application..."
exec waitress-serve --port=8000 config.wsgi:application
=======
gunicorn --workers 4 config.wsgi:application --bind 0.0.0.0:443

>>>>>>> 2c8169cef62a25e803300f5ec79a956e5f23e110
