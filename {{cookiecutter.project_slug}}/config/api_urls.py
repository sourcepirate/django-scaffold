from django.urls import re_path, include

app_name = "api_urls"

urlpatterns = [
    re_path(r"^users/", include("{{cookiecutter.project_slug}}.users.api_urls"), name="users"),
]
