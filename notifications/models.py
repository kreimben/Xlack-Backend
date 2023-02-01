from django.db import models

from chat.models import Chat
from chat_channel.models import ChatChannel
from notifications.manager import NotificationManger
from xlack import settings


class Notification(models.Model):
    """
    Notification model
    Many Notification per one chat
    """
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
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="notification_chat",
        default=None,  # Have to allow blank, if want to test without chat
        null=True,
        blank=True,
    )

    had_read = models.BooleanField(default=False)

    objects = NotificationManger()

    def __str__(self):
        return f"{self.sender} ({self.chat}) to {self.receiver} read: {self.had_read}"
