from rest_framework import serializers


class DMCreateSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    target_user_id = serializers.IntegerField()
