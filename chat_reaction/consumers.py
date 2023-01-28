from channels.db import database_sync_to_async

from chat_channel.models import ChatChannel

from chat_reaction.models import ChatReaction
from chat_reaction.serializers import ChatReactionSerializer

from websocket.AuthWebsocketConsumer import AuthWebsocketConsumer

from rest_framework.serializers import ValidationError


class ReactionConsumer(AuthWebsocketConsumer):
    chat_channel: ChatChannel | None = None

    @database_sync_to_async
    def create_or_add(self, chat_id, icon):

        icon = icon.encode("unicode_escape").decode("ascii")

        reaction, is_created = ChatReaction.objects.get_or_create(
            chat_id=chat_id, icon=icon
        )

        if self.user not in reaction.reactors.all():
            reaction.reactors.add(self.user)

            serial = ChatReactionSerializer(reaction)

            return serial.data
        else:
            raise ValidationError(f"{self.user} was found in reactors (Duplication)")

    @database_sync_to_async
    def remove_or_delete(self, chat_id, icon):

        icon = icon.encode("unicode_escape").decode("ascii")

        try:
            reaction = ChatReaction.objects.get(chat_id=chat_id, icon=icon)
        except ChatReaction.DoesNotExist:
            raise ChatReaction.DoesNotExist("There is no reaction like that")

        if self.user not in reaction.reactors.all():
            raise ValidationError(f"{self.user} was not found in reactors (Not Found)")
        else:
            reaction.reactors.remove(self.user)
            if reaction.reactors.count() == 0:
                serial = ChatReactionSerializer(reaction)
                tmp_icon = serial.icon
                reaction.delete()
                dic = dict(chat_id=chat_id, icon=tmp_icon, count=0, reactors=None)
                return dic
            else:
                reaction.save()
                serial = ChatReactionSerializer(reaction)
        return serial.data

    async def after_auth(self):
        await super().after_auth()

    async def before_accept(self):
        kwargs = self.scope["url_route"]["kwargs"]
        self.room_group_name = kwargs["chat_channel_hashed_value"]

    async def after_accept(self):
        try:
            self.chat_channel = await ChatChannel.objects.aget(
                hashed_value__exact=self.room_group_name
            )
        except ChatChannel.DoesNotExist:
            await self.send_json(
                {
                    "success": False,
                    "msg": "No such chat channel. (Wrong chat channel hashed value)",
                },
                close=True,
            )

    async def from_client(self, content, **kwargs):

        if content.get("create", None) is True:
            icon = content.get("icon")
            chat_id = content.get("chat_id")

            reaction = await self.create_or_add(chat_id, icon)

            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "reaction.broadcast", "reaction": reaction},
            )

        elif content.get("remove", None) is True:
            icon = content.get("icon")
            chat_id = content.get("chat_id")

            reaction = await self.remove_or_delete(chat_id, icon)

            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "reaction.broadcast", "reaction": reaction},
            )

    async def reaction_broadcast(self, event):
        """
        This function send reaction to every body in this group.
        """
        await self.send_json(
            {"creation": event["creation"], "reaction": event["reaction"]}
        )
