import json

from channels.db import database_sync_to_async
from rest_framework.serializers import ValidationError

from chat_channel.models import ChatChannel
from chat_reaction.models import ChatReaction
from chat_reaction.serializers import ChatReactionSerializer
from websocket.AuthWebsocketConsumer import AuthWebsocketConsumer


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
        __icon = icon.encode("unicode_escape").decode("ascii")

        try:
            reaction = ChatReaction.objects.get(chat_id=chat_id, icon=__icon)
        except ChatReaction.DoesNotExist:
            raise ValidationError("There is no reaction like that")

        if self.user not in reaction.reactors.all():
            raise ValidationError(f"{self.user} was not found in reactors (Not Found)")
        else:
            reaction.reactors.remove(self.user)
            serial = ChatReactionSerializer(reaction)
            if reaction.reactors.count() == 0:
                reaction.delete()
                return {"chat_id": chat_id, "icon": icon, "reactors": [], "count": 0}
            return serial.data

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

    async def after_auth(self):
        await super().after_auth()

    async def from_client(self, content, **kwargs):
        mode = content.get("mode", None)
        if mode == "create":
            icon = content.get("icon")
            chat_id = content.get("chat_id")
            try:
                reaction = await self.create_or_add(chat_id, icon)
            except ValidationError as e:
                await self.send_json({"success": False, "msg": e.detail})
            else:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type": "reaction.broadcast", "reaction": reaction},
                )
        elif mode == "delete":
            icon = content.get("icon")
            chat_id = content.get("chat_id")
            try:
                reaction = await self.remove_or_delete(chat_id, icon)
            except ValidationError as e:
                await self.send_json({"success": False, "msg": e.detail})
            else:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type": "reaction.broadcast", "reaction": reaction},
                )
        else:
            await self.send_json(
                {
                    "success": False,
                    "msg": 'Mode should be "create" or "delete". Please refer to "form" below',
                    "form": json.dumps(
                        {
                            "mode": "create or delete",
                            "icon": "some icon as raw",
                            "chat_id": "chat id",
                        }
                    ),
                }
            )

    async def reaction_broadcast(self, event):
        """
        This function send reaction to every body in this group.
        """
        await self.send_json({"success": True, "reaction": event["reaction"]})
