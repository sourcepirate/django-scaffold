from django.contrib import admin
from {{cookiecutter.project_slug}}.users.models import User

# Register your models here.
admin.site.register([User])
