import requests
from django.conf import settings

from .metrics import collect_local_metrics
from .models import VPSServer


def fetch_server_metrics(server: VPSServer):
    """Fetch metrics for a VPS server. Uses local collection for the local server."""
    if server.is_local:
        try:
            return collect_local_metrics()
        except Exception as exc:
            return _error_payload(str(exc))

    if not server.is_active:
        return _error_payload("Server is disabled")

    try:
        response = requests.get(
            server.metrics_url(),
            headers={"X-API-Token": server.api_token},
            timeout=settings.METRICS_REQUEST_TIMEOUT,
        )
        if response.status_code == 401:
            return _error_payload("Invalid API token")
        if response.status_code != 200:
            return _error_payload(f"HTTP {response.status_code}")
        data = response.json()
        data["status"] = "online"
        return data
    except requests.Timeout:
        return _error_payload("Connection timed out")
    except requests.ConnectionError:
        return _error_payload("Unable to connect")
    except Exception as exc:
        return _error_payload(str(exc))


def fetch_all_metrics():
    """Fetch metrics for every active VPS server."""
    servers = VPSServer.objects.filter(is_active=True)
    return [(server, fetch_server_metrics(server)) for server in servers]


def _error_payload(message):
    return {
        "status": "error",
        "error": message,
        "hostname": "—",
        "cpu_percent": 0,
        "memory": {"percent": 0, "used_gb": 0, "total_gb": 0, "available_gb": 0},
        "disk": {"percent": 0, "used_gb": 0, "total_gb": 0, "free_gb": 0},
        "load_avg": [0, 0, 0],
        "uptime_seconds": 0,
    }
