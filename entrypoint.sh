#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py init
daphne -b 0.0.0.0 -p 8000 door.asgi:application
