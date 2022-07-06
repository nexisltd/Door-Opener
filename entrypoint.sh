#!/bin/sh

python manage.py migrate

gunicorn --bind 0.0.0.0:8000 door.wsgi -w 4 -k uvicorn.workers.UvicornWorker