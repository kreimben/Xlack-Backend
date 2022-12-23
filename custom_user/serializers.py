from rest_framework import serializers

from custom_user.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'display_name', 'title', 'phone_number', 'profile_image']