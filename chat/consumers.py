from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class ChatConsumer(JsonWebsocketConsumer):

    def connect(self):
        self.channel_id = self.scope['url_route']['kwargs']['channel_id']
        print(f'channel_id: {self.channel_id}')
        self.room_group_name = f'chat_{self.channel_id}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def receive_json(self, content, **kwargs):
        """
        This function JUST receive messages.
        After that, You should send message to group.
        """
        print(f'content type: {type(content)}')
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'speak',
                'user': self.scope['user'].username,
                'message': content['message']
            }
        )

    def speak(self, event):
        """
        This function speaks message to every body in this group.
        """
        self.send_json({
            'user': event['user'],
            'message': event['message']
        })

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            str(code)
        )
