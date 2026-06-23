import socket
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class VPSServer(models.Model):
    """A VPS instance monitored by this installation."""

    name = models.CharField(max_length=100, help_text="Friendly display name")
    base_url = models.URLField(
        help_text="Base URL of the VPS Pilot instance, e.g. https://vps2.example.com"
    )
    api_token = models.CharField(
        max_length=128,
        help_text="METRICS_API_TOKEN configured on the remote VPS",
    )
    is_local = models.BooleanField(
        default=False,
        help_text="Whether this is the server running this application",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_local", "name"]
        verbose_name = "VPS Server"
        verbose_name_plural = "VPS Servers"

    def __str__(self):
        suffix = " (local)" if self.is_local else ""
        return f"{self.name}{suffix}"

    def clean(self):
        if self.is_local and VPSServer.objects.filter(is_local=True).exclude(pk=self.pk).exists():
            raise ValidationError({"is_local": "Only one local VPS server is allowed."})

    def metrics_url(self):
        return f"{self.base_url.rstrip('/')}{reverse('metrics_api')}"

    @classmethod
    def ensure_local_server(cls):
        """Create or update the local VPS entry on startup."""
        token = settings.METRICS_API_TOKEN
        if not token:
            token = uuid.uuid4().hex
            # Token must be set in env for production; we still register locally.

        hostname = socket.gethostname()
        base_url = f"http://127.0.0.1:8000"

        local, _created = cls.objects.get_or_create(
            is_local=True,
            defaults={
                "name": f"{hostname} (local)",
                "base_url": base_url,
                "api_token": token,
            },
        )
        if not _created:
            local.api_token = token
            local.save(update_fields=["api_token", "updated_at"])
        return local
