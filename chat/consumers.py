import ujson

from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(JsonWebsocketConsumer):

    def connect(self):
        self.channel_id = self.scope['url_route']['kwargs']['channel_id']
        print(f'channel_id: {self.channel_id}')
        self.room_group_name = f'chat_{self.channel_id}'

    async def connect(self):
        self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = ujson.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            ujson.dumps({
                'message': message
            }))

    # async def disconnect(self, code):
    #     pass
