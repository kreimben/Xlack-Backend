from django.contrib.auth.models import User
from rest_framework import serializers

from user_profile.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'thumbnail_url']
