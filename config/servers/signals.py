from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def ensure_local_vps(sender, **kwargs):
    if sender.name != "servers":
        return
    from .models import VPSServer

    VPSServer.ensure_local_server()
