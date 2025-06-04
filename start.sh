#!/bin/bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear
gunicorn graph_project.wsgi:application --bind 0.0.0.0:$PORT
