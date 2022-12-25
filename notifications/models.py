# notifications/models.py
from django.db import models
from notifications.manager import NotificationManger

from xlack import settings

from chat_channel.models import ChatChannel

# from chat.models import Chat


"""
=== Logic of Notification Creation

1. Get Notification by signal

2. Parsing it,
    Who send it?
    in where ?
    who receive it ?

3. Manage it,
    if the receiver is offline, save it to DB
    elif the receiver is online,
        don't save, just notify

"""

"""
=== Logic of Notification Use

1. User connected

2. Get user's info 

3. Notification internal signal, user is online

4. Get Notification by Group (Source of Notification)
    and send them to User

5. if user read, modify it

"""


class Notification(models.Model):
    """
    Notification model
    Many Notification per one chat
    """

    # id will be created automatically

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notification"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notification"
    )
    channel = models.ForeignKey(
        ChatChannel,
        on_delete=models.CASCADE,
        related_name="notification",
        default=None,
        blank=True,  # if it's a DM
    )

    had_read = models.BooleanField(default=False)

    objects = NotificationManger

    # do we have to add datetime?
    # to filter more?
    # created_at = models.DateTimeField(auto_now_add=True)

    # TODO: adding messege as foreignkey, to reverse refer
    # messege = models.ForeignKey(
    #     Chat, on_delete=models.CASCADE, related_name="notfication"
    # )
