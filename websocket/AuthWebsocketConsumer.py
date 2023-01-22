import json
from abc import abstractmethod, ABC

import rest_framework_simplejwt
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from rest_framework_simplejwt.exceptions import TokenError

from AuthHelper import AuthHelper
from custom_user.models import CustomUser


class AuthWebsocketConsumer(AsyncJsonWebsocketConsumer, ABC):
    user: CustomUser | None = None  # To save current user information.

    async def connect(self):
        await self.before_accept()
        await self.accept()
        await self.after_accept()

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
                    await self.after_auth()
                    await self.channel_layer.group_add(
                        self.room_group_name,
                        self.channel_name
                    )
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

    @abstractmethod
    async def from_client(self, content, **kwargs):
        """
        Deal with client's general message without auth.
        """
        pass

    @abstractmethod
    async def before_accept(self):
        """
        save `self.room_group_name` and etc...
        """
        pass

    @abstractmethod
    async def after_accept(self):
        pass

    @abstractmethod
    async def after_auth(self):
        await self.send_json({
            'success': True,
            'msg': 'Success to auth',
            'user_id': self.user.id
        })

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
