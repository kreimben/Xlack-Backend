# notifications/models.py
from django.db import models

from xlack import settings

from workspace.models import Workspace
from chat.models import Chat


class Notification(models.Model):
    """
    Notification model
    Many Notification per one chat
    """

    # id will be created automatically

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notification"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notification"
    )
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="notification",
        default=None,
        blank=True,  # if it's a DM
    )
    messege_id = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name="notfication"
    )

    had_read = models.BooleanField(default=False)

    # do we have to add datetime?
    # to filter more?
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"
