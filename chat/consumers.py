import ujson

from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(JsonWebsocketConsumer):

class ChatConsumer(WebsocketConsumer):

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
