from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import User

from chat.models import Chat
from chat_channel.models import ChatChannel


class ChatConsumer(AsyncJsonWebsocketConsumer):
    # TODO: Implement auth jobs for JWT.
    async def connect(self):
        self.channel_id = self.scope['url_route']['kwargs']['channel_id']
        # print(f'channel_id: {self.channel_id}')
        self.room_group_name = f'chat_{self.channel_id}'

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

        @database_sync_to_async
        def get_channel(channel_id):
            return ChatChannel.objects.get(id=channel_id)

        @database_sync_to_async
        def create_chat(message, chatter, channel):
            return Chat(message=message, chatter=chatter, channel=channel).save()

        @database_sync_to_async
        def get_user(user_id):
            return User.objects.get(id=user_id)

        user: User = await get_user(content['user_id'])
        # print(f'user: {user}')
        # print(f'user id: {content["user_id"]}')
        channel = await get_channel(self.channel_id)
        await create_chat(content['message'], user, channel)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'speak',
                'user': content['user_id'],
                'message': content['message']
            }
        )

    async def speak(self, event):
        """
        This function speaks message to every body in this group.
        """
        await self.send_json({
            'user': event['user'],
            'message': event['message']
        })

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        raise StopConsumer()
