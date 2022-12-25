from channels.generic.websocket import JsonWebsocketConsumer
from rest_framework_simplejwt.exceptions import TokenError

from notifications.utils import find_user, find_access_token


class NotificationsConsumer(JsonWebsocketConsumer):
    def connect(self):

        try:
            # find user by access_token
            access_token = find_access_token(self.scope)
            if access_token is None:
                raise TokenError("Authorization token not found!")
        except TokenError as tokenError:
            print(f"{tokenError}")
            return

        user, user_id = find_user(access_token)

    def accept(self, subprotocol=None):
        pass

    def receive_json():
        pass

    def disconnect():
        pass
