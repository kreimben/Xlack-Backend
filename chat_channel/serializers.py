from rest_framework import serializers

from chat_channel.models import ChatChannel


class ChatChannelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChatChannel
        fields = ['name', 'id']
