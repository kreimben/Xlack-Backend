from django.conf import settings
from django.db import models

from chat_channel.models import ChatChannel


class Chat(models.Model):
    message = models.TextField(null=False, blank=False)
    chatter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False)
    channel = models.ForeignKey(ChatChannel, on_delete=models.CASCADE, null=False, blank=False, related_name='chat')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.channel} 채널의 {self.message}'
