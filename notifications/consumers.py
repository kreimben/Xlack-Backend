import json

from channels.db import database_sync_to_async

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.exceptions import StopConsumer

from rest_framework_simplejwt.exceptions import TokenError

from notifications.utils import find_user, find_access_token
from notifications import api

# TODO: add logging


@database_sync_to_async
def _create_notification_list(user_id):
    api.create_notification_list(user_id)


@database_sync_to_async
def _read(user_id, sender, channel):
    api.read(receiver=user_id, sender=sender, channel=channel)


class NotificationsConsumer(AsyncJsonWebsocketConsumer):
    @database_sync_to_async
    def _refresh(self, user_id):
        list_of_notification = _create_notification_list(user_id)
        return json.dumps(list_of_notification)

    async def connect(self):
        # check auth token
        try:
            access_token = find_access_token(self.scope)
            if access_token is None:
                raise TokenError
        except TokenError:

            print("Authorization token not found!")
            self.close()
            return

        _, user_id = find_user(access_token)
        list_of_notification = _create_notification_list(user_id)

        self.accept()

        self.send_json(json.dumps(list_of_notification))

    # TODO: choose when to refash

    async def receive_json(self, content):
        """
        Find user model using access token
        and
        """
        access_token = find_access_token(self.scope)  # Don't check about access token.
        _, user_id = find_user(
            access_token
        )  # May return None if access token is expired.
        if user_id is None:
            self.send_json(
                content={"msg": "access token is expired or invalid."}, close=True
            )

        if content.sender and content.channel == None:
            self.send_json(content={"msg": "sender and channel are invalid."})

        else:
            _read(receiver=user_id, sender=content.sender, channel=content.channel)

            new_notifications = self._refresh(user_id)

            self.send_json(content=new_notifications)

    def disconnect(self, code):
        raise StopConsumer()
