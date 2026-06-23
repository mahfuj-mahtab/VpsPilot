import platform
import time

import psutil
from django.utils import timezone


def _bytes_to_gb(value):
    return round(value / (1024 ** 3), 2)


def collect_local_metrics():
    """Gather system metrics from the machine running this app."""
    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)

    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    cpu_percent = psutil.cpu_percent(interval=0.5)
    load_avg = list(psutil.getloadavg()) if hasattr(psutil, "getloadavg") else [0, 0, 0]

    return {
        "hostname": platform.node(),
        "platform": platform.platform(),
        "cpu_count": psutil.cpu_count() or 1,
        "cpu_percent": round(cpu_percent, 1),
        "memory": {
            "total_gb": _bytes_to_gb(memory.total),
            "used_gb": _bytes_to_gb(memory.used),
            "available_gb": _bytes_to_gb(memory.available),
            "percent": round(memory.percent, 1),
        },
        "disk": {
            "total_gb": _bytes_to_gb(disk.total),
            "used_gb": _bytes_to_gb(disk.used),
            "free_gb": _bytes_to_gb(disk.free),
            "percent": round(disk.percent, 1),
        },
        "load_avg": [round(v, 2) for v in load_avg],
        "uptime_seconds": uptime_seconds,
        "collected_at": timezone.now().isoformat(),
        "status": "online",
    }
