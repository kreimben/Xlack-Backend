from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from chat_channel.models import ChatChannel
from custom_user.serializers import CustomUserSerializer, CustomUserNameSerializer
from workspace.models import Workspace


class ChatChannelModifySerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    members = CustomUserSerializer(many=True, read_only=True)
    admins = CustomUserSerializer(many=True, read_only=True)
    hashed_value = serializers.CharField(read_only=True)

    class Meta:
        model = ChatChannel
        fields = ['name', 'id', 'description', 'hashed_value', 'members', 'admins']


class ChatChannelFixDescSerializer(serializers.ModelSerializer):
    members = CustomUserSerializer(many=True, read_only=True)
    admins = CustomUserSerializer(many=True, read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = ChatChannel
        fields = ['id', 'name', 'description', 'hashed_value', 'members', 'admins']


class ChatChannelMembersModifyRequestSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    members_usernames = CustomUserNameSerializer(many=True)
    hashed_value = serializers.CharField(read_only=True)

    class Meta:
        model = ChatChannel
        fields = ['id', 'name', 'description', 'hashed_value', 'members_usernames']


class ChatChannelAdminsModifyRequestSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    admins_usernames = CustomUserNameSerializer(many=True)
    hashed_value = serializers.CharField(read_only=True)

    class Meta:
        model = ChatChannel
        fields = ['id', 'name', 'description', 'hashed_value', 'admins_usernames']


class ChatChannelSerializer(serializers.ModelSerializer):
    description = serializers.CharField(read_only=True)
    is_dm = serializers.BooleanField(read_only=True)
    members = CustomUserSerializer(many=True, read_only=True)
    admins = CustomUserSerializer(many=True, read_only=True)
    hashed_value = serializers.CharField(read_only=True)

    class Meta:
        model = ChatChannel
        fields = ['id', 'name', 'hashed_value', 'description', 'members', 'admins', 'is_dm']

    def create(self, validated_data):
        hashed_value = ''
        for key, value in validated_data.get('workspace').items():
            hashed_value = value

        workspace = get_object_or_404(Workspace, hashed_value__exact=hashed_value)

        return ChatChannel.objects.create(
            name=validated_data.get('name'),
            workspace=workspace
        )
