from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("server-info/", views.server_info, name="server_info"),
    path("server-info/<int:pk>/refresh/", views.server_metrics_partial, name="server_metrics_partial"),
    path("api/metrics/", views.metrics_api, name="metrics_api"),
]
