#!/bin/sh
set -e
python -c "import django; print('Django', django.get_version())"
python manage.py makemigrations demo --noinput || true
python manage.py migrate --noinput || true
python manage.py seed || true
exec python manage.py runserver 0.0.0.0:8000 --noreload
