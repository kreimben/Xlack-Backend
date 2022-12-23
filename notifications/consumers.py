# date time might be need to access db with
from datetime import datetime

from channels.generic.websocket import JsonWebsocketConsumer
from rest_framework_simplejwt.exceptions import TokenError

from status.consumers import _find_user, _find_access_token

# signals to add notificationlist's total number,
# within connection, the notification will got
# summary by event,
# and, anounce to client by time interval
from django.core import signals


class NotificationsConsumer(JsonWebsocketConsumer):

    def connect(self):
        # the user connected, so have to find user's belongs,
        # like, the workspace, channels, 

        try:
            # find user by access_token
            access_token = _find_access_token(self.scope)
            if access_token is None:
                raise TokenError("Authorization token not found!")
        except TokenError as tokenError:
            print(f"{tokenError}")
            return

        user, user_id = _find_user(access_token)


    # implement for client had read notification,
    # so have to modify that
    def accept(self, subprotocol=None):
        # async to sync to modify DB 
        async def 
    

    # recived json..
    def receive_json():
        
    def disconnect()
