from django.contrib import admin

from subscribers.models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "is_admin")
    list_filter = ("is_active", "is_admin")
    search_fields = ("name", "info")
