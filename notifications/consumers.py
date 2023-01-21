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
        notifications: [Notification] = Notification.objects.filter(receiver_id=receiver_id,
                                                                    channel__hashed_value=channel_hashed_value)
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
        self.room_group_name = f'{self.user.id}'
        list_of_notification = await self._get_notification_list(self.user.id)
        await self.send_json({
            'success': True,
            'msg': 'Success to auth',
            'user_id': self.user.id,
            'notifications': list_of_notification
        })

    async def from_client(self, content, **kwargs):
        if content.get('refresh', None) is True:
            r = await self._get_notification_list(self.user.id)
            await self.send_json(r)
        elif content.get('channel_hashed_value', None) is not None:
            channel_hashed_value = content.get('channel_hashed_value', None)
            await self._read_notification(receiver_id=self.user.id, channel_hashed_value=channel_hashed_value)
            await self.send_json({'msg': 'OK'})

    async def notifications_broadcast(self, event):
        r = await self._get_notification_list(event.get('user_id', None))
        await self.send_json(r)
