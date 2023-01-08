from django.contrib import admin

from chat_channel.models import ChatChannel


@admin.register(ChatChannel)
class ChatChannelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'hashed_value', 'description', 'is_dm', 'workspace', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['is_dm', 'workspace']
