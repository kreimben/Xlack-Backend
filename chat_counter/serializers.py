from rest_framework import serializers

from chat_channel.models import ChatChannel


class ChatCounterSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    channel = serializers.PrimaryKeyRelatedField(many=False, read_only=True)


class ChatReadInfoSerializer(serializers.ModelSerializer):
    counter = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    user = serializers.PrimaryKeyRelatedField()
    most_recent_chat = serializers.PrimaryKeyRelatedField()
