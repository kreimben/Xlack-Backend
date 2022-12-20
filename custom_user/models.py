from django.db import models

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    display_name = models.CharField(max_length=50, default='')
    title = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, default='')

    class Meta:
        verbose_name = 'CustomUser'
        verbose_name_plural = 'CustomUsers'
