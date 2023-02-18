from django.db import models

from chat_channel.models import ChatChannel
from file.models import File
from xlack import settings


class Chat(models.Model):
    message = models.TextField(null=False, blank=False)
    file = models.ForeignKey(File, on_delete=models.SET_NULL, null=True, blank=True)
    chatter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False)
    channel = models.ForeignKey(ChatChannel, on_delete=models.CASCADE, null=False, blank=False, related_name='chat')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'
        ordering = ['-id']

    def __str__(self):
        return f'{self.channel} 채널의 {self.message}'


class ChatBookmark(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='bookmarks')
    issuer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Chat Bookmark'
        verbose_name_plural = 'Chat Bookmarks'

    def __str__(self):
        return f'{self.chat} ({self.issuer})'
