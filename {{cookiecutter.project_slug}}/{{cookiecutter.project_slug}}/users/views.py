from {{cookiecutter.project_slug}}.celery_app import celery_app
from django.http import HttpResponse

# Create your views here.
def health(request):
    celery_app.send_task("health_check")
    return HttpResponse("200OK")
