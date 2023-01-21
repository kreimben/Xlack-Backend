from chat.models import Chat
from chat_channel.models import ChatChannel
from file.models import File
from websocket.AuthWebsocketConsumer import AuthWebsocketConsumer


class ChatConsumer(AuthWebsocketConsumer):
    chat_channel: ChatChannel | None = None

    async def before_accept(self):
        kwargs = self.scope["url_route"]["kwargs"]
        self.room_group_name = kwargs['chat_channel_hashed_value']

    async def after_accept(self):
        try:
            self.chat_channel = await ChatChannel.objects.aget(hashed_value__exact=self.room_group_name)
        except ChatChannel.DoesNotExist:
            await self.send_json({
                'success': False,
                'msg': 'No such chat channel. (Wrong chat channel hashed value)'
            }, close=True)

    async def after_auth(self):
        await super().after_auth()

    async def from_client(self, content, **kwargs):
        f = None
        file_id = content.get('file_id', None)
        if file_id is not None:
            try:
                f = await File.objects.aget(id=file_id)
            except File.DoesNotExist as e:
                await self.send_json({'msg': str(e)}, close=True)

        chat: Chat = await Chat.objects.acreate(message=content['message'],
                                                chatter=self.user,
                                                channel=self.chat_channel,
                                                file=f if f is not None else None)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.broadcast',
                'username': self.user.username,
                'user_id': self.user.id,
                'message': chat.message,
                'file_id': file_id
            }
        )

    async def chat_broadcast(self, event):
        """
        This function speaks message to every body in this group.
        """
        await self.send_json({
            'username': event['username'],
            'user_id': event['user_id'],
            'message': event['message'],
            'file_id': event['file_id']
        })
