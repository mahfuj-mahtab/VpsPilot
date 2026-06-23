from django.shortcuts import redirect
from django.urls import path

from . import views


def root_redirect(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("dashboard")
    return redirect("login")


urlpatterns = [
    path("", root_redirect, name="root"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
