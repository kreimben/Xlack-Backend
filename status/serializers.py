from rest_framework import serializers

from custom_user.serializers import CustomUserSerializer
from status.models import UserStatus
from workspace.serializers import BaseWorkspaceSerializer


class UserStatusSerializer(serializers.ModelSerializer):
    workspace = BaseWorkspaceSerializer(read_only=True)
    user = CustomUserSerializer()

    class Meta:
        model = UserStatus
        fields = ['message', 'icon', 'user', 'until', 'workspace']


class ManyUserStatusSerializer(serializers.Serializer):
    user_status = UserStatusSerializer(many=True)

    class Meta:
        fields = ['user_status']

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
