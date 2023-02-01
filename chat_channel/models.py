from uuid import uuid4

from django.db import models
from django.db.models import Prefetch

from custom_user.models import CustomUser
from workspace.models import Workspace
from xlack import settings


class ChannelManager(models.Manager):
    def get_queryset(self):
        user_queryset = CustomUser.objects.all()
        return super().get_queryset() \
            .select_related('workspace') \
            .filter(is_dm=False) \
            .prefetch_related(Prefetch('members', queryset=user_queryset)) \
            .prefetch_related(Prefetch('admins', queryset=user_queryset))


class DMManager(models.Manager):
    def get_queryset(self):
        user_queryset = CustomUser.objects.all()
        return super().get_queryset() \
            .select_related('workspace') \
            .filter(is_dm=True) \
            .prefetch_related(Prefetch('members', queryset=user_queryset)) \
            .prefetch_related(Prefetch('admins', queryset=user_queryset))


# The reason I named `ChatChannel` is avoiding confusion with `django channels`.
class ChatChannel(models.Model):
    name = models.CharField(max_length=50)
    hashed_value = models.CharField(db_index=True, max_length=10, unique=True, default=str(uuid4())[:8])
    is_dm = models.BooleanField(default=False)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE,
                                  null=False, blank=False,
                                  related_name='chat_channel')
    description = models.TextField(null=True, blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_channel_members')
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_channel_admins')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    channel_objects = ChannelManager()
    dm_objects = DMManager()

    class Meta:
        verbose_name = 'Channel'
        verbose_name_plural = 'Channels'

    def __str__(self):
        return f'{self.name} ({self.hashed_value} / {self.workspace})'
