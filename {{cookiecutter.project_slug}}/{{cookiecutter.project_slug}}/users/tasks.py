import logging

from {{cookiecutter.project_slug}}.celery_app import celery_app

log = logging.getLogger("django")


@celery_app.task(name="health_check")
def health_check(*args):
    log.info("Health checking celery")
