from asgiref.sync import sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from AuthHelper import AuthHelper, AccessTokenNotIncludedInHeader
from chat.models import Chat
from chat_channel.models import ChatChannel
from custom_user.models import CustomUser
from file.models import File


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        kwargs = self.scope["url_route"]["kwargs"]
        self.room_group_name = kwargs['chat_channel_hashed_value']

        try:
            await sync_to_async(AuthHelper.find_user)(self.scope)
        except AccessTokenNotIncludedInHeader:
            print(f'access token was not in header.')
            return
        except CustomUser.DoesNotExist:
            print(f'No such user.')
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive_json(self, content, **kwargs):
        """
        This function JUST receive messages.
        After that, You should send message to group.
        """
        user: CustomUser = await sync_to_async(AuthHelper.find_user)(self.scope)
        channel: ChatChannel = await ChatChannel.objects.aget(hashed_value__exact=self.room_group_name)
        f = None
        file_id = content.get('file_id', None)
        if file_id is not None:
            try:
                f = await File.objects.aget(id=file_id)
            except File.DoesNotExist as e:
                await self.send_json({'msg': str(e)}, close=True)

        chat: Chat = await Chat.objects.acreate(message=content['message'],
                                                chatter=user,
                                                channel=channel,
                                                file=f if f is not None else None)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.broadcast',
                'username': user.username,
                'user_id': user.id,
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

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        raise StopConsumer()
