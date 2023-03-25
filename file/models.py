from django.db import models

from xlack import settings


def upload_file(instance, filename):
    return f'media/file/user_{instance.uploaded_by.id}/{filename}'


class File(models.Model):
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_file')
    file = models.FileField(upload_to=upload_file)
    file_name = models.CharField(max_length=1000, blank=True, null=True) # For searching.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.url
