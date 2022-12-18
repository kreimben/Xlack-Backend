from django.contrib import admin

from status.models import UserStatus


@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'icon', 'message', 'workspace', 'until']
    search_fields = ['user_id', 'message']
