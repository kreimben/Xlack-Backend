from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from AuthHelper import AuthHelper, AccessTokenNotIncludedInHeader
from custom_user.models import CustomUser
from notifications import api


class NotificationsConsumer(AsyncJsonWebsocketConsumer):
    @database_sync_to_async
    def _create_notification_list(self, user_id):
        return api.get_notification_list(user_id)

    @database_sync_to_async
    def _read(self, user_id, sender, channel):
        return api.read_notification_list(
            receiver=user_id, sender=sender, channel=channel
        )

    @database_sync_to_async
    def _refresh(self, user_id):
        list_of_notification = self._create_notification_list(user_id)
        return list_of_notification

    async def connect(self):
        # check auth token
        try:
            user = await sync_to_async(AuthHelper.find_user)(self.scope)
            if user is None:
                print(f"{user=}")
                return
        except AccessTokenNotIncludedInHeader:
            print(f"access token was not in header.")
            return
        except CustomUser.DoesNotExist:
            print(f"No such user.")
            return

        list_of_notification = await self._create_notification_list(user.id)

        await self.accept()

        await self.send_json(content=list_of_notification)

    async def receive_json(self, content):
        """
        Find user model using access token
        and
        """
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

        if content.refresh:
            new_notifications = await self._refresh(user.id)
            await self.send_json(content=new_notifications)

        else:
            if content.sender and content.channel == None:
                await self.send_json(content={"msg": "sender and channel are invalid."})
            else:
                await self._read(
                    receiver=user.id, sender=content.sender, channel=content.channel
                )
                new_notifications = await self._refresh(user.id)

                await self.send_json(content=new_notifications)

    def disconnect(self, code):
        raise StopConsumer()
