from rest_framework import viewsets, permissions

from user_profile.models import UserProfile
from user_profile.serializers import UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']
