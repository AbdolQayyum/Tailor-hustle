#!/bin/bash

set -e

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database makemigrations
echo "Apply database makemigrations"
python manage.py makemigrations

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
# python manage.py runserver 0.0.0.0:8000

# and add this at the end
exec "$@"