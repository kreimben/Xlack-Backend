from django.contrib import admin

from chat_reaction.models import ChatReaction

from chat_reaction.serializers import Util


@admin.register(ChatReaction)
class ChatReactionAdmin(admin.ModelAdmin):

    def icon_repr(self, obj):
        return Util.to_repr(obj.icon)

    list_display = ['id', 'chat', 'icon_repr']
