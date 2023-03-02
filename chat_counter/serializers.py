from rest_framework import serializers

from chat.serializers import ChatSerializer
from chat_channel.models import ChatChannel
from chat_channel.serializers import ChatChannelSerializer
from custom_user.serializers import CustomUserSerializer

from .models import Counter, ReadInfo


class ReadInfoSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(many=False, read_only=True)
    most_recent_chat = ChatSerializer(many=False, read_only=True)

    class Meta:
        model = ReadInfo
        fields = ["user", "most_recent_chat"]


class ChatCounterSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    channel = ChatChannelSerializer(many=False, read_only=True)
    readinfo = ReadInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Counter

    def create(self, validated_data):
        channel = validated_data.pop("channel")
        counter = Counter.objects.get_or_create(channel=channel)

        user = validated_data.pop("user")
        most_recent_chat = validated_data.pop("most_recent_chat")

        readinfo = ReadInfo.objects.create(
            counter=counter,
            user=user,
            most_recent_chat=most_recent_chat,
            **validated_data
        )

        return {channel: channel, readinfo: readinfo}

    def update(self, instance, validated_data):
        channel = validated_data.pop("channel")
        counter = Counter.objects.get_or_create(channel=channel)

        user = validated_data.pop("user")
        readinfo = ReadInfo.objects.get(
            counter=counter,
            user=user,
        )

        most_recent_chat = validated_data.pop("most_recent_chat")
