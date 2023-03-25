from rest_framework import serializers

from chat.serializers import ChatSerializer
from custom_user.serializers import CustomUserSerializer
from file.serializers import FileSerializer


class SearchSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    type = serializers.ChoiceField(
        choices=(
            ('chat', 'chat'),
            ('file_name', 'file_name'),
            ('user', 'user')
        ),
        read_only=True)
    chat = ChatSerializer(read_only=True)
    file = FileSerializer(read_only=True)
    user = CustomUserSerializer(read_only=True)