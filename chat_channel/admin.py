from django.contrib import admin

from chat_channel.models import ChatChannel


@admin.register(ChatChannel)
class ChatChannelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ChatChannel._meta.get_fields()]
    search_fields = ['name']
