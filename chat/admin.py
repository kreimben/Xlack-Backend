from django.contrib import admin

from chat.models import Chat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'message', 'chatter', 'file', 'channel', 'created_at']
    search_fields = ['message', 'channel', 'chatter']
    ordering = ['-created_at']
