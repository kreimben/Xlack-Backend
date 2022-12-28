# notifications/models.py
from django.db import models
from notifications.manager import NotificationManger

from xlack import settings

from chat_channel.models import ChatChannel


class Notification(models.Model):
    """
    Notification model
    Many Notification per one chat
    """

    # id will be created automatically

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_receiver",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_sender",
    )
    channel = models.ForeignKey(
        ChatChannel,
        on_delete=models.CASCADE,
        related_name="notification_channel",
        default=None,
        null=True,
        blank=True,  # if it's a DM
    )

    had_read = models.BooleanField(default=False)

    objects = NotificationManger()

    def __str__(self):
        return f"{self.sender}@{self.channel} send to {self.receiver},read={self.had_read}]"
