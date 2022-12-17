from rest_framework import serializers

from workspace.models import Workspace


# TODO: custom user 모델 만들어서 serializer 따로 만들고, 밑에 있는 각 serializer 에 넣기.
class BaseWorkspaceSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Workspace
        exclude = ['id', 'members']


class NameWorkspaceSerializer(BaseWorkspaceSerializer):
    hashed_value = serializers.CharField(read_only=True)


class HashWorkspaceSerializer(BaseWorkspaceSerializer):
    name = serializers.CharField(read_only=True)
