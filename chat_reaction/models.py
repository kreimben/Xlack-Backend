from django.db import models
from chat.models import Chat
from xlack import settings


class ChatReaction(models.Model):
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name='reaction')
    reactors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='reaction_reactors',
        blank=True
    )
    icon = models.CharField(max_length=20, null=False, blank=False)

    class Meta:
        verbose_name = 'Chat Reaction'
        verbose_name_plural = 'Chat Reactions'
        constraints = [
            models.UniqueConstraint(
                fields=['chat', 'icon'], name='unique_reaction')
        ]

    def __str__(self):
        return f'({self.id}-{self.icon})-({self.chat}-{self.reactors.all()}) '
