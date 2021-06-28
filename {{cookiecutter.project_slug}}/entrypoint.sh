#!/bin/bash

python manage.py migrate
gunicorn config.wsgi:application --bind=$HOST:$PORT -w 1 -k gevent --log-level debug --max-requests-jitter 2000 \
         --max-requests 1500 
