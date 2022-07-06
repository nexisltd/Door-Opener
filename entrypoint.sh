#!/bin/sh

python manage.py migrate

gunicorn door.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000