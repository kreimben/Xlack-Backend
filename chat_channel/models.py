from django.db import models

from workspace.models import Workspace
from xlack import settings


# The reason I named `ChatChannel` is avoiding confusion with `django channels`.
class ChatChannel(models.Model):
    name = models.CharField(max_length=50)
    hashed_value = models.CharField(max_length=10, unique=True)
    is_dm = models.BooleanField(default=False)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, null=False, blank=False,
                                  related_name='chat_channel')
    description = models.TextField(null=True, blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_channel_members')
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_channel_admins')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Channel'
        verbose_name_plural = 'Channels'

    def __str__(self):
        return f'{self.name} ({self.hashed_value} / {self.workspace})'
