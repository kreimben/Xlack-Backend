from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from chat.models import Chat, ChatBookmark, ChatReaction
from custom_user.serializers import CustomUserSerializer


class ChatSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    channel = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    has_bookmarked = serializers.BooleanField(read_only=True)
    chatter = CustomUserSerializer(many=False, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        data = {}
        for key, value in validated_data:
            if key != 'has_bookmarked':
                data[key] = value
        return Chat(**data)

    def update(self, instance, validated_data):
        instance.channel = validated_data.get('channel', instance.channel)
        instance.chatter = validated_data.get('chatter', instance.chatter)
        return instance


class ChatBookmarkSerializer(serializers.ModelSerializer):
    chat_id = serializers.PrimaryKeyRelatedField(
        many=False, queryset=Chat.objects.all())
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ChatBookmark
        fields = ['chat_id', 'created_at']


class ChatReactionSerializer(serializers.Serializer):
    chat_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    reactors = CustomUserSerializer(many=True, read_only=True)
    icon = serializers.CharField(max_length=10, read_only=True)

    def create(self, validated_data):
        return ChatReaction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.reactors = validated_data.get('reactors', instance.reactors)
        instance.chat = validated_data.get('chat', instance.chat)
        instance.icon = validated_data.get('reaction', instance.icon)
        return instance

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=ChatReaction.objects.all(),
                fields=['chat', 'icon']
            )
        ]
