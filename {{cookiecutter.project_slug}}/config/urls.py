from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(r"v1/", include("config.api_urls", namespace="api")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
