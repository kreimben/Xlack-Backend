from rest_framework import serializers

from custom_user.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'display_name', 'title', 'phone_number', 'profile_image']


class CustomUserNameSerializer(CustomUserSerializer):
    email = serializers.CharField(read_only=True)
    display_name = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    phone_number = serializers.CharField(read_only=True)
    profile_image = serializers.CharField(read_only=True)
