from rest_framework import serializers

from chat.models import Chat, ChatBookmark
from chat_reaction.serializers import ChatReactionSerializer
from custom_user.serializers import CustomUserSerializer
from file.serializers import FileSerializer


class ChatSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    message = serializers.CharField(read_only=True)
    channel = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    has_bookmarked = serializers.BooleanField(read_only=True)
    chatter = CustomUserSerializer(many=False, read_only=True)
    reaction = ChatReactionSerializer(many=True)  # For optimizing codes. And no performance issues either.
    file = FileSerializer(read_only=True)
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


class BookmarkedChatsSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    message = serializers.CharField(read_only=True)
    channel = serializers.PrimaryKeyRelatedField(many=False,
                                                 read_only=True)  # ChatChannelSerializer(many=False, read_only=True)
    chatter = CustomUserSerializer(many=False, read_only=True)
    reaction = ChatReactionSerializer(many=True)
    file = FileSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Chat
        fields = '__all__'


class ChatBookmarkSerializer(serializers.ModelSerializer):
    chat_id = serializers.PrimaryKeyRelatedField(many=False, queryset=Chat.objects.all())
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ChatBookmark
        fields = ['chat_id', 'created_at']
