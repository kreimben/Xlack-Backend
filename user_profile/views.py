from allauth.socialaccount.models import SocialAccount
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from user_profile.models import UserProfile
from user_profile.serializers import UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    http_method_names = ['get']
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'user_id'

    def list(self, request, *args, **kwargs):
        """
        모든 유저의 프로필입니다.
        """
        social_users = SocialAccount.objects.all()

        for user in social_users:
            UserProfile.objects.get_or_create(
                user_id=user.user_id,
                github_id=user.extra_data['id'],
                bio=user.extra_data['bio'],
                thumbnail_url=user.extra_data['avatar_url']
            )

        s = [UserProfileSerializer(user) for user in self.get_queryset()]

        return Response([user.data for user in s])

    def retrieve(self, request, *args, **kwargs):
        """
        특정 유저의 프로필입니다.
        식별자: `user_id`
        """
        user_id = self.kwargs.get('user_id')
        social_user = SocialAccount.objects.get(user_id=user_id)
        user, _ = UserProfile.objects.get_or_create(
            user_id=social_user.user_id,
            github_id=social_user.extra_data['id'],
            bio=social_user.extra_data['bio'],
            thumbnail_url=social_user.extra_data['avatar_url']
        )
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
