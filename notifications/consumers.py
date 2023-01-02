from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from AuthHelper import AuthHelper, AccessTokenNotIncludedInHeader
from custom_user.models import CustomUser
from notifications import api


class NotificationsConsumer(AsyncJsonWebsocketConsumer):
    @database_sync_to_async
    def _get_notification_list(self, user_id):
        return api.get_notification_list(user_id)

    @database_sync_to_async
    def _read(self, user_id, sender, channel):
        return api.read_notification_list(
            receiver=user_id, sender=sender, channel=channel
        )

    async def connect(self):
        self.room_group_name = ''
        # check auth token
        try:
            user = await sync_to_async(AuthHelper.find_user)(self.scope)
            if user is None:
                print(f"{user=}")
                return
            self.room_group_name = f'{user.id}'
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
        except AccessTokenNotIncludedInHeader:
            print(f"access token was not in header.")
            return
        except CustomUser.DoesNotExist:
            print(f"No such user.")
            return

        list_of_notification = await self._get_notification_list(user.id)

        await self.accept()

        await self.send_json(content=list_of_notification)

    async def receive_json(self, content, **kwargs):
        try:
            user = await sync_to_async(AuthHelper.find_user)(self.scope)
        except AccessTokenNotIncludedInHeader:
            print(f"access token was not in header.")
            await self.send_json(
                content={"msg": "access token was not in header."}, close=True
            )
            return
        except CustomUser.DoesNotExist:
            print(f"No such user.")
            await self.send_json(content={"msg": "No such user."}, close=True)
            return

        if content.get('refresh', None) == True:
            r = await self._get_notification_list(user.id)
            await self.send_json(r)
        elif content.get('had_read', None) is not None and content.get('notification_id', None) is not None:
            ...

    async def notifications_broadcast(self, event):
        r = await self._get_notification_list(event.get('user_id', None))
        await self.send_json(r)

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
