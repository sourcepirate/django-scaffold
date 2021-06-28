#!/bin/sh
celery -A config.worker worker -c 2