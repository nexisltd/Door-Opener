#!/bin/sh

python manage.py migrate

gunicorn --bind 0.0.0.0:8000 door.asgi -w 10 -k uvicorn.workers.UvicornWorker
