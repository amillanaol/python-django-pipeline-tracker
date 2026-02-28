from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path

urlpatterns = [
    path("favicon.ico", lambda request: HttpResponse(status=204)),
    path("admin/", admin.site.urls),
    path("api/", include("src.infrastructure.web.api.urls")),
]
