import json

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .services import fetch_all_metrics, fetch_server_metrics
from .models import VPSServer
from config.utils.custom_decorator import staff_or_superuser_required

# def superuser_required(view):
#     return user_passes_test(lambda u: u.is_superuser, login_url="login")(view)


@login_required
@staff_or_superuser_required
def dashboard(request):
    return render(request, "servers/dashboard.html")


@login_required
@staff_or_superuser_required
def server_info(request):
    metrics_data = fetch_all_metrics()
    context = {
        "servers_metrics": metrics_data,
        "servers_metrics_json": json.dumps(
            [
                {
                    "id": server.pk,
                    "name": server.name,
                    "is_local": server.is_local,
                    "metrics": metrics,
                }
                for server, metrics in metrics_data
            ]
        ),
    }
    return render(request, "servers/server_info.html", context)


@login_required
@staff_or_superuser_required
@require_GET
def server_metrics_partial(request, pk):
    """HTMX-friendly partial refresh for a single server card."""
    server = VPSServer.objects.get(pk=pk)
    metrics = fetch_server_metrics(server)
    return render(
        request,
        "servers/partials/server_card.html",
        {"server": server, "metrics": metrics},
    )


@require_GET
def metrics_api(request):
    """Public metrics endpoint protected by API token (for remote polling)."""
    token = request.headers.get("X-API-Token", "")
    expected = settings.METRICS_API_TOKEN

    if not expected or token != expected:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    from .metrics import collect_local_metrics

    return JsonResponse(collect_local_metrics())
