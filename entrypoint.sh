#!/bin/sh

python manage.py migrate

# gunicorn --bind 0.0.0.0:8000 door.asgi -w 4 -k uvicorn.workers.UvicornWorker --timeout 600
daphne -b 0.0.0.0 -p 8000 door.asgi:application
