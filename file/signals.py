import os

import boto3
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from file.models import File


def load_signal():
    print('file signals loaded!')


@receiver(pre_delete, sender=File)
def before_delete_file(sender: File, **kwargs):
    """
    If you delete files on admin or anywhere, Files still preserve on bucket.
    So for deleting that original files too, Connect signals to django.
    """
    s3_client = boto3.client('s3',
                             aws_access_key_id=os.getenv('AWS_S3_ACCESS_KEY_ID'),
                             aws_secret_access_key=os.getenv('AWS_S3_SECRET_ACCESS_KEY'),
                             endpoint_url='https://' + os.getenv('AWS_S3_CUSTOM_DOMAIN'))

    file: File = kwargs.get('instance', None)

    response = s3_client.delete_object(
        Bucket=os.getenv('AWS_STORAGE_BUCKET_NAME'),
        Key=file.file.name
    )
