from rest_framework import serializers

from notifications.models import Notification


class NotificationSerialser(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "sender", "receiver", "channel", "had_read"]
