from django.db import models


# The reason I named `ChatChannel` is avoiding confusion with `django channels`.
class ChatChannel(models.Model):
    # Should we make chatted user field?
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Channel'
        verbose_name_plural = 'Channels'

    def __str__(self):
        return self.name
