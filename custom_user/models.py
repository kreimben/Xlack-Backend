from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.db import models


def upload_img(instance, filename):
    return f'media/profile_image/user_{instance.id}/{filename}'


class CustomUser(AbstractUser):
    display_name = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    profile_image = models.ImageField(upload_to=upload_img, null=True, blank=True)

    # Should have  to include profile image field.

    def __str__(self):
        return f'{self.username} ({self.display_name} / {self.title})'
