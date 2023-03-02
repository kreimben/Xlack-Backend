from django.db import models

from chat.models import Chat
from chat_channel.models import ChatChannel
from xlack import settings


class Counter(models.Model):
    channel = models.ForeignKey(
        ChatChannel,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_reading = models.BooleanField(default=False)
    most_recent_chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Read information"
        verbose_name_plural = "Read informations"
        ordering = ["-most_recent_chat__id"]

    def __str__(self):
        return f"{self.user}@{self.channel}:{self.most_recent_chat.id}"
