#!/bin/sh

python manage.py migrate

gunicorn door.wsgi:application --bind 0.0.0.0:8000
