from rest_framework import serializers

from file.models import File


class FileSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = File
        fields = ['id', 'uploaded_by', 'file', 'created_at', 'updated_at']
