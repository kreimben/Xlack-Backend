from django.contrib import admin

from notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["id", "sender", "receiver", "channel", "had_read"]
    search_fields = ["sender", "receiver", "channel"]
