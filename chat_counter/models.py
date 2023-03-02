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
        related_name="chat",
    )

    class Meta:
        verbose_name = "Chat Counter"
        verbose_name_plural = "Chat Counters"

    def __str__(self):
        return f"{self.channel}>{self.readinfo}"


class ReadInfo(models.Model):
    counter = models.ForeignKey(Counter, models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    most_recent_chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name="readinfo"
    )

    class Meta:
        verbose_name = "Read information"
        verbose_name_plural = "Read informations"
        ordering = ["-most_recent_chat.id"]

    def __str__(self):
        return f"{self.user}({self.most_recent_chat})"
