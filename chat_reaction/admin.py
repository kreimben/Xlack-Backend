from django.contrib import admin

from chat_reaction.models import ChatReaction


@admin.register(ChatReaction)
class ChatReactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat', 'icon']
