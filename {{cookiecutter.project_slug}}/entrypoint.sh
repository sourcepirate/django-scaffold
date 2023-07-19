#!/bin/bash

python manage.py migrate
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn config.wsgi:application --bind=0.0.0.0:8000 -w 1 -k gthread --max-requests-jitter 2000 --max-requests 1500