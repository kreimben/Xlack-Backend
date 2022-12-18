from rest_framework import serializers

from status.models import UserStatus
from workspace.serializers import BaseWorkspaceSerializer


class UserStatusSerializer(serializers.ModelSerializer):
    workspace = BaseWorkspaceSerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # TODO: Custom User 만들면 serializer도 같이 만들어서 여기에 넣기.

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
