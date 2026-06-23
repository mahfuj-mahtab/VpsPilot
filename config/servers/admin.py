from django.contrib import admin

from .models import VPSServer


@admin.register(VPSServer)
class VPSServerAdmin(admin.ModelAdmin):
    list_display = ("name", "base_url", "is_local", "is_active", "created_at")
    list_filter = ("is_local", "is_active")
    search_fields = ("name", "base_url")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("name", "base_url", "api_token")}),
        ("Status", {"fields": ("is_local", "is_active")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if obj and obj.is_local:
            readonly.extend(["is_local", "base_url"])
        return readonly
