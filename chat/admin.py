from django.contrib import admin

from chat.models import Chat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Chat._meta.get_fields()]
    search_fields = ['name']
