from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from chat_channel.models import ChatChannel
from workspace.models import Workspace


class ChatChannelSerializer(serializers.ModelSerializer):
    # workspace = HashWorkspaceSerializer()

    class Meta:
        model = ChatChannel
        fields = ['name', 'id', ]  # 'workspace']

    def create(self, validated_data):
        hashed_value = ''
        for key, value in validated_data.get('workspace').items():
            hashed_value = value

        workspace = get_object_or_404(Workspace, hashed_value__exact=hashed_value)

        return ChatChannel.objects.create(
            name=validated_data.get('name'),
            workspace=workspace
        )
