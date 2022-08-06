from rest_framework import serializers

from chat.models import Chat


class ChatSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    chatter_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Chat
        fields = '__all__'
