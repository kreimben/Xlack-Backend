from rest_framework import serializers

from custom_user.serializers import CustomUserSerializer
from workspace.models import Workspace


class BaseWorkspaceSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    members = CustomUserSerializer(many=True, read_only=True)

    class Meta:
        model = Workspace
        exclude = ['id']


class NameWorkspaceSerializer(BaseWorkspaceSerializer):
    hashed_value = serializers.CharField(read_only=True)


class HashWorkspaceSerializer(BaseWorkspaceSerializer):
    name = serializers.CharField(read_only=True)
