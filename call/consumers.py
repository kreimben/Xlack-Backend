import json

import rest_framework_simplejwt
from rest_framework_simplejwt.exceptions import TokenError
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from custom_user.models import CustomUser

from asgiref.sync import sync_to_async

from Hasher import Hasher

from AuthHelper import AuthHelper

class CallConsumer(AsyncJsonWebsocketConsumer):
    user: CustomUser | None = None
    user_channel= None # one channel for one user
    group_channel= None # group channel for group call

    async def connect(self):
        # Check user access token to validate auth.
        await self.send_json({
            'msg': 'Give me user access token. Just input access token value.',
            'format': json.dumps({
                'authorization': '{access_token}'
            })
        })

    async def receive_json(self, content, **kwargs):
        """
        Client should authorize to server only first time.
        """
        if content.get('authorization', None) is not None:
            if self.user is None:
                try:
                    self.user, _ = await sync_to_async(AuthHelper.find_user_by_access_token)(
                        content.get('authorization'))
                    self.user_channel= f'call_{self.user.id}'

                except rest_framework_simplejwt.exceptions.TokenError as e:
                    await self.send_json({
                        'success': False,
                        'msg': f'{str(e)}'
                    }, close=True)
                except CustomUser.DoesNotExist:
                    await self.send_json({
                        'success': False,
                        'msg': 'No such user'
                    }, close=True)
            else:
                await self.send_json({
                    'msg': 'You already have auth info in server.\nIf you want to re-auth, Just re-connect server.',
                    'user': f'user_id: {self.user.id}'
                })
        else:
            await self.from_client(content, **kwargs)

    async def after_auth(self):

        await self.channel_layer.group_add(
            self.user_channel,
            self.channel_name
        )

        await self.send_json({
            'success': True,
            'msg': 'Success to auth',
            'user_id': self.user.id
        })

    async def from_client(self, content, **kwargs):
        info = """
        request format : 
            {
                'request': 'call.new' # start new call
                         : 'call.accept' # accpet call
                         : 'call.reject' # reject call
                         : 'group.new' # manage new group call 
                         : 'group.invite' # invite one user to existing group
                         : 'group.accept' # accept invitation 
                         : 'group.reject' # reject group
                         : 'group.quit' # quit group
            }
        if request is none, send sdp exchange info request
        """
        request = content.get('request',None)

        if request is not None:
            request = request.split('.')

            # manage one to one call
            if request[0]=='call':
                self.call(content,request[1])
            # manage group call
            elif request[0]=='group':
                self.group_call(content,request[1])
            else:
                self.send_json({
                    "error":"invalid request",
                    "format":info
                    })
        else:
            self.manage_offer(content) # manage sdp


    # manage one to one call
    async def call(self,content,kind):
        target = content.get('target',None)
        request = content.get('request',None)
        peer = self.user.id
        if target == None:
            await self.send_json({
            "error": "target is none, failed to start new call"
            })
            return
        if kind == 'new':
            msg = f" User id:{peer} want to call"
        elif kind == 'accept':
            msg = f" User id:{peer} accepted to call"
        elif kind == 'reject':
            msg = f" User id:{peer} rejected to call"
        else:
            await self.send_json({
                "error": f"invalid request : {kind}, failed to {kind}"
            })
            return

        await self.channel_layer.group_send(
                f'call_{target}',
                {
                    "type":"send.event",
                    "request":request,
                    "peer":peer,
                    "msg":msg,
                })

    # manage group request
    async def group_call(self,content,kind):
        target = content.get('target',None)
        request = content.get('request',None)
        group = content.get('group',None)
        peer = self.user.id

        if target == None and group == None:
            await self.send_json({
                "error": "target and group are both none"
            })
            return
        elif target != None:
            target = f'call_{target}'

        scope = group or target

        if kind == 'new':
            msg = f" User id:{peer} want to promote to group call"
            self.group_channel = f"call_group_{Hasher.hash(peer)}"
            self.channel_layer.group_add(self.group_channel,self.channel_name)
            group = self.group_channel
            await self.send_json({
                "msg" : f"new group created :{self.group_channel}",
                "group" : self.group_channel
                })
        elif kind == 'invite':
            msg = f" User id:{peer} invited to group call"
            if group == None:
                await self.send_json({
                "error": "Group is none, failed to invite"
                })
                return
        elif kind == 'accept':
            if self.group_channel == None:
                msg = f" User id:{peer} accepted to invitation"
                self.group_channel = group
                self.channel_layer.group_add(self.group_channel,self.channel_name)
            else:
                await self.send_json({
                "error": "Already in group, failed to join"
                })
                return
        elif kind == 'reject':
            msg = f" User id:{peer} rejected to invitation"
        elif kind == 'quit':
            msg = f" User id:{peer} quit to group call"
            await self.channel_layer.group_send(
                scope,
                {
                    "type":"send.group.event",
                    "request":request,
                    "peer":peer,
                    "msg":msg,
                    "group":group,
                })
            self.channel_layer.group_discard(self.group_channel,self.channel_name)
            self.group_channel = None
            return
        else:
            await self.send_json({
                "error": f"invalid request : {kind}, failed to {kind}"
            })
            return

        await self.channel_layer.group_send(
                scope,
                {
                    "type":"send.group.event",
                    "request":request,
                    "peer":peer,
                    "msg":msg,
                    "group":group,
                })

    async def manage_offer(self,content, **kwargs):
        request_type = content.get('type',None)
        target = content.get('target',None)
        group = content.get('group',None)
        peer = self.user.id

        if target == None and group == None:
            await self.send_json({
                "error": "target and group are both none"
            })
            return
        elif target != None:
            target = f'call_{target}'

        scope = group or target

        await self.channel_layer.group_send(
            scope,
            {
                "type":request_type,
                "peer":peer,
                "sdp":content.get('sdp',None),
            })

    async def send_event(self, event):
        await self.send_json(
            {
                'type':event['type'],
                'request':event['request'],
                'peer': event['peer'],
                'msg':event['msg'],
            })

    async def send_group_event(self, event):
        await self.send_json(
            {
                'type':event['type'],
                'request':event['request'],
                'peer': event['peer'],
                'msg':event['msg'],
                'group':event['group']
            })

    async def sdp_offer(self, event):
       await self.send_json(
            {
                'type': 'sdp.offer',
                'peer': event['peer'],
                'sdp':event['sdp'],
            }
        )
    async def sdp_answer(self, event):
       await self.send_json(
            {
                'type': 'sdp.answer',
                'peer': event['peer'],
                'sdp':event['sdp'],
            }
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.user_channel,
            self.group_channel,
            self.channel_name
        )
