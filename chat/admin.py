from django.contrib import admin

from chat.models import Chat, ChatBookmark


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'message', 'chatter', 'file', 'channel', 'created_at']
    search_fields = ['message', 'channel', 'chatter']
    ordering = ['-created_at']


@admin.register(ChatBookmark)
class ChatBookmarkAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat', 'issuer', 'created_at']
    search_fields = ['id', 'chat', 'issuer']
    list_filter = ['issuer']
