from allauth.socialaccount.models import SocialAccount
from rest_framework import viewsets, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from user_profile.models import UserProfile
from user_profile.serializers import UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'user_id'

    def list(self, request, *args, **kwargs):
        """
        본인의 프로필입니다.
        """
        user_id = request.user.id
        social_user = get_object_or_404(SocialAccount, **{'user_id': user_id})
        user, _ = UserProfile.objects.get_or_create(
            user_id=social_user.user_id,
            github_id=social_user.extra_data['id'],
            bio=social_user.extra_data['bio'],
            thumbnail_url=social_user.extra_data['avatar_url']
        )

        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        본인의 프로필을 생성합니다.
        """
        user_profile = UserProfile.objects.create(user=request.user)

        user_profile.display_name = request.data.get('display_name')
        user_profile.title = request.data.get('title')
        user_profile.phone_number = request.data.get('phone_number')
        user_profile.save()

        p = self.get_serializer(user_profile)
        return Response(p.data)

    def update(self, request, *args, **kwargs):
        """
        프로필을 수정합니다.
        """
        user_profile = UserProfile.objects.get(user=request.user)

        user_profile.display_name = request.data.get('display_name')
        user_profile.title = request.data.get('title')
        user_profile.phone_number = request.data.get('phone_number')
        user_profile.thumbnail_url = request.data.get('thumbnail_url')

        user_profile.save()

        s = self.get_serializer(user_profile)

        return Response(s.data)

    def destroy(self, request, *args, **kwargs):
        """
        프로필을 삭제합니다.
        """
        user_profile = UserProfile.objects.get(user=request.user)

        user_profile.delete()
        return Response({'success': True, 'message': 'Successfully deleted!'}, status=status.HTTP_200_OK)
