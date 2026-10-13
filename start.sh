#!/bin/sh
set -e

python manage.py migrate --no-input
exec gunicorn dumpstermap.wsgi --bind 0.0.0.0:8000
