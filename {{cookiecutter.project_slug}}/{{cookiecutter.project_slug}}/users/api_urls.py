from django.urls import re_path, path
from {{cookiecutter.project_slug}}.users import api

app_name = "users"
urlpatterns = [
    path(
        "google/login",
        api.GoogleLoginAPI.as_view(),
        name="social_auth_google",
    ),
    path(
        "facebook/login",
        api.FacebookLoginAPI.as_view(),
        name="social_auth_facebook",
    ),
    re_path(r"^(?P<pk>[0-9]+)/$", api.UserAPI.as_view(), name="userapi"),
    re_path(r"^user$", api.UserAPI.as_view(), name="userapi"),
]
