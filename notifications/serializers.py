# notifications/serializers.py

from rest_framework import serializers
from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):

    """
    Notification serializer,
    per one Notification model
    """

    class Meta:
        model = Notification
        field = ["id", "receiver", "sender", "workspace", "had_read"]

    def create(self, validated_data):
        """
        Creation of notification instance
        """

    def update(self, instance, validated_data):
        """
        Update of notification instance
        Don't use this directly
        """
        super().update()


class NotificationListSerializer(serializers.ListSerializer):
    """
    Notification list
    belongs to one unique user via one of sources of notifications
    """

    pass
