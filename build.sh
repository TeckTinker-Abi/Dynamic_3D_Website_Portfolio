#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create static directory if not exists
mkdir -p static

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
