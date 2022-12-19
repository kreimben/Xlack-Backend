from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models

from workspace.models import Workspace


class UserStatus(models.Model):
    message = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    until = models.DateTimeField()
    user = models.OneToOneField(AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='status')  # If original row is exist, Update it.
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='user_status')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        This method is override for emoji.
        """
        self.icon = str(self.icon.encode('unicode_escape'))
        super(UserStatus, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'User Status'
        verbose_name_plural = 'User Status'

    def __str__(self):
        return f'{self.message} by {self.user}'
