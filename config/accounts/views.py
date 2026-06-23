from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("dashboard")

    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user is None:
            error = "Invalid username or password."
        elif not user.is_superuser:
            error = "Access denied. Only superadmin accounts can sign in."
        elif not user.is_active:
            error = "This account has been deactivated."
        else:
            login(request, user)
            return redirect("dashboard")

    return render(request, "accounts/login.html", {"error": error})


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")
