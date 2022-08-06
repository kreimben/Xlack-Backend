from django.contrib.auth.models import User
from django.db import models

from chat_channel.models import ChatChannel


class Chat(models.Model):
    content = models.TextField(null=False, blank=False)
    chatter_id = models.ForeignKey(User, on_delete=models.PROTECT, default=1, blank=False)
    channel_id = models.ForeignKey(ChatChannel, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.channel_id} : {self.content}'
