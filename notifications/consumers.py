from channels.db import database_sync_to_async

from notifications import api
from notifications.models import Notification
from websocket.AuthWebsocketConsumer import AuthWebsocketConsumer


class NotificationsConsumer(AuthWebsocketConsumer):
    @database_sync_to_async
    def _get_notification_list(self, user_id):
        return api.get_notification_list(user_id)

    @database_sync_to_async
    def _read(self, user_id, sender, channel):
        return api.read_notification_list(
            receiver=user_id, sender=sender, channel=channel
        )

    @database_sync_to_async
    def _read_notification(self, receiver_id: int, channel_hashed_value: str):
        notifications: list[Notification] = list(
            Notification.objects.filter(
                receiver_id=receiver_id, channel__hashed_value=channel_hashed_value
            )
        )
        for noti in notifications:
            noti.had_read = True
            noti.save()

    async def before_accept(self):
        # No need to implement this behavior
        pass

    async def after_accept(self):
        # No need to implement this behavior
        pass

    async def after_auth(self):
        self.room_group_name = f"{self.user.id}"
        list_of_notification = await self._get_notification_list(self.user.id)
        await self.send_json(
            {
                "success": True,
                "msg": "Success to auth",
                "user_id": self.user.id,
                "notifications": list_of_notification,
            }
        )

    async def from_client(self, content, **kwargs):
        if content.get("refresh", None) is True:
            r = await self._get_notification_list(self.user.id)
            await self.send_json(r)
        elif (hashed_value := content.get("channel_hashed_value", None)) is not None:
            await self._read_notification(
                receiver_id=self.user.id, channel_hashed_value=hashed_value
            )
            await self.send_json({"success": True, "msg": "OK"})

    async def notifications_broadcast(self, event):
        target, recent_chat = event.get("user_id", None), event.get("recent_chat_id")
        if target is not None:
            r = await self._get_notification_list(target)
            await self.send_json({"recent_chat_id": recent_chat, "notifications": r})
        else:
            raise ValueError(
                "Notification.consumer>>broadcasting target is None", target
            )

    async def disconnect(self, code):
        if self.room_group_name:
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
