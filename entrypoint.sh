#!/bin/sh
python manage.py migrate --noinput
python manage.py collectstatic --noinput

if [ "$RUN_SEED" = "true" ]; then
    python manage.py seed_database
    python manage.py load_geojson
fi

gunicorn --bind 0.0.0.0:8000 uksc_backend_django.wsgi:application
