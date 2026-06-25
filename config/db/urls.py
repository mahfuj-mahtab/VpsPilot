from django.urls import path

from .views import db_dashboard

urlpatterns = [
    path("postgres/dashboard/", db_dashboard, name="db_dashboard"),
]
