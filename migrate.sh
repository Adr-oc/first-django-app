#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Applying migrations..."
python manage.py migrate --run-syncdb

echo "Migrations completed successfully!"
