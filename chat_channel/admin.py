from django.contrib import admin

from chat_channel.models import ChatChannel


@admin.register(ChatChannel)
class ChatChannelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'hashed_value', 'description', 'created_at', 'updated_at']
    search_fields = ['name']
