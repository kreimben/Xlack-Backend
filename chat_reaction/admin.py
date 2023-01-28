from django.contrib import admin

from chat_reaction.models import ChatReaction
from chat_reaction.serializers import Util


@admin.register(ChatReaction)
class ChatReactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat', 'get_icon', 'get_reactors']

    def get_icon(self, obj):
        return Util.to_repr(obj.icon)

    def get_reactors(self, obj: ChatReaction):
        return ', '.join([str(user) for user in obj.reactors.all()])
