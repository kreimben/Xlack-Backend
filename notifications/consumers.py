from channels.db import database_sync_to_async

from notifications import api
from notifications.models import Notification
from websocket.AuthWebsocketConsumer import AuthWebsocketConsumer


class NotificationsConsumer(AuthWebsocketConsumer):
    @database_sync_to_async
    def _get_unread_notifications(self, user):
        return api.get_notification_list(user)

    @database_sync_to_async
    def _read_notification(self, user, channel):
        return api.read_notification_list(receiver=user, channel=channel)

    async def before_accept(self):
        # No need to implement this behavior
        pass

    async def after_accept(self):
        # No need to implement this behavior
        pass

    async def after_auth(self):
        self.room_group_name = f"{self.user.id}"
        noti = await self._get_unread_notifications(self.user.id)
        await self.send_json(
            {
                "success": True,
                "msg": "Success to auth",
                "user_id": self.user.id,
                "notifications": noti,
            }
        )

    async def from_client(self, content, **kwargs):
        if content.get("refresh", None) is True:
            r = await self._get_unread_notifications(self.user.id)
            await self.send_json(r)
        elif (hashed_value := content.get("channel_hashed_value", None)) is not None:
            await self._read_notification(
                receiver=self.user, channel_hashed_value=hashed_value
            )
            await self.send_json({"success": True, "msg": "OK"})

    async def notifications_broadcast(self, event):
        recent_chat = event.get("recent_chat_id")
        channel_hashed_value = event.get("channel_hashed_value")

        if self.user is not None:
            r = await self._get_unread_notifications(self.user)
            await self.send_json(
                {
                    "recent_chat_id": recent_chat,
                    "notifications": r,
                    "channel_hashed_value": channel_hashed_value,
                }
            )
        else:
            raise ValueError(
                "Notification.consumer>>broadcasting target(self.user) is None"
            )

    async def disconnect(self, code):
        if self.room_group_name:
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
