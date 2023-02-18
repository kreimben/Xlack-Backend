from django.db import models

from Hasher.Hasher import Hasher
from xlack import settings


class Workspace(models.Model):
    name = models.CharField(max_length=100, unique=True)
    hashed_value = models.CharField(db_index=True, default=Hasher.hash, max_length=10, unique=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='joined_workspaces')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Workspace'
        verbose_name_plural = 'Workspaces'

    def __str__(self):
        return f'{self.name}'
