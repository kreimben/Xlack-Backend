from websocket.AuthWebsocketConsumer import AuthWebsocketConsumer

class CallConsumer(AuthWebsocketConsumer):
    room_group_name = None

    async def before_accept(self):
        pass

    async def after_accept(self):
        pass

    async def after_auth(self):
        self.room_group_name = f'call_{self.user.id}'
        await super().after_auth()

    async def from_client(self, content, **kwargs):
        type = content.get('type',None)
        if type =="offer":
            target = content.get('target',None)
            if target == None:
                await self.send_json({
                    "error": "target is none"
                })
                return
            await self.channel_layer.group_send(
                    f'call_{target}',
                    {
                        "type":"offer",
                        "peer":self.user.id,
                        "sdp":content.get('sdp',None),
                    })

        if type =="answer":
            target = content.get('target',None)
            if target == None:
                await self.send_json({
                    "error": "target is none"
                })
                return
            await self.channel_layer.group_send(
                    f'call_{target}',
                    {
                        "type":"answer",
                        "peer":self.user.id,
                        "sdp":content.get('sdp',None),
                    })


    async def offer(self, event):
       await self.send_json(
            {
                'type': 'offer',
                'peer': event['peer'],
                'sdp':event['sdp'],
            }
        )
    async def answer(self, event):
       await self.send_json(
            {
                'type': 'answer',
                'peer': event['peer'],
                'sdp':event['sdp'],
            }
        )
