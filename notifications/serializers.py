# notification/serializers.py
from rest_framework import serializers
from notifications.models import Notification


"""
Notification serializer,
per one Notification model
"""
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        field = ["id", "receiver", "sender", "workspace", "had_read"]

    def create(self,...


"""
Notification list
belongs to one unique user via one of sources of notifications
"""
class NotificationListSerializer(serializers.ListSerializer):
