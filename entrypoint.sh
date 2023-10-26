#!/bin/bash

# Collect static files
python quizhero-app/manage.py collectstatic --no-input

# Start App
gunicorn -c gunicorn_config.py quizhero_app.wsgi:application
