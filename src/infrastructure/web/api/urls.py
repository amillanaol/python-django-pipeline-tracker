from django.urls import include, path
from rest_framework.routers import DefaultRouter

from src.infrastructure.web.api.views import (
    PipelineRunViewSet,
    VulnerabilityViewSet,
    dashboard_summary,
)

router = DefaultRouter()
router.register(r"pipelines", PipelineRunViewSet, basename="pipeline")
router.register(r"vulnerabilities", VulnerabilityViewSet, basename="vulnerability")

urlpatterns = [
    path("", include(router.urls)),
    path("dashboard/", dashboard_summary, name="dashboard-summary"),
]
