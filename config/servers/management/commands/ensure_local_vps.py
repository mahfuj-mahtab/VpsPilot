from django.core.management.base import BaseCommand

from servers.models import VPSServer


class Command(BaseCommand):
    help = "Ensure the local VPS server entry exists in the database."

    def handle(self, *args, **options):
        server = VPSServer.ensure_local_server()
        self.stdout.write(self.style.SUCCESS(f"Local VPS registered: {server.name}"))
