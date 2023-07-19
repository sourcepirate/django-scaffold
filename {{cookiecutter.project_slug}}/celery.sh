#!/bin/bash
celery -A {{cookiecutter.project_slug}}.celery_app worker -P gevent --loglevel=INFO --concurrency=8 -O fair -n cel_app_worker