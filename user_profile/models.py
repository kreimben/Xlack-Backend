from xlack import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    github_id = models.CharField(max_length=20, default='0')
    bio = models.TextField(null=True, blank=True)
    thumbnail_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    display_name = models.CharField(max_length=50, default='')
    title = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, default='')

    class Meta:
        ordering = ['created_at', 'user_id']
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f'{self.user}'
