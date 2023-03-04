from rest_framework import serializers

from .models import Counter


class ChatCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counter
        fields = "__all__"
