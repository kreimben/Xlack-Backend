from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

from chat_channel.models import ChatChannel
from chat_channel.serializers import ChatChannelSerializer, ChatChannelModifySerializer, ChatChannelFixDescSerializer, \
    ChatChannelMembersModifyRequestSerializer, \
    ChatChannelAdminsModifyRequestSerializer
from custom_user.models import CustomUser
from workspace.models import Workspace


class ChatChannelView(generics.CreateAPIView,
                      generics.ListAPIView,
                      generics.UpdateAPIView):
    queryset = ChatChannel.objects.all()
    serializer_class = ChatChannelSerializer
    http_method_names = ['get', 'post', 'patch']
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            self.serializer_class = ChatChannelModifySerializer
        elif self.request.method == 'PATCH':
            self.serializer_class = ChatChannelFixDescSerializer

        return self.serializer_class

    def get_queryset(self):
        hashed_value = self.kwargs.get('workspace__hashed_value', None)
        result = self.queryset.filter(workspace__hashed_value=hashed_value)
        return result

    def post(self, request: Request, *args, **kwargs):
        """
        `workspace_hashed_value`를 입력하면 해당 workspace의 `chat_channel`을 추가합니다.
        `name`에는 만들 채널의 이름을 넣으십시오.
        채널을 생성하면 `members`안에는 자동으로 만든 사람의 정보가 포함 됩니다.
        채널 만든 사람은 `admins`안에 역시 자동으로 들어갑니다.
        """
        if request.data.get('name', None) is None:
            return Response({'msg': 'name field is not filled.'}, status=status.HTTP_400_BAD_REQUEST)

        hashed_value = self.kwargs.get('workspace__hashed_value', None)

        workspace = Workspace.objects.get(hashed_value__exact=hashed_value)
        chat_channel = ChatChannel.objects.create(name=request.data.get('name', None),
                                                  description=request.data.get('description', None),
                                                  workspace=workspace)
        chat_channel.members.add(request.user)
        chat_channel.admins.add(request.user)

        serializer = self.get_serializer(chat_channel)
        return Response(serializer.data)

    def get(self, request: Request, *args, **kwargs):
        """
        `workspace_hashed_value`를 입력하면 해당 workspace의 `chat_channel`들이 나옵니다.
        """
        chat_channels = self.get_queryset()
        serializer = self.get_serializer(chat_channels, many=True)

        return Response(data=serializer.data)

    def patch(self, request: Request, *args, **kwargs):
        """
        `ChatChannel`의 설명 문구를 바꾸기 위한 엔드포인트 입니다.
        이걸로 `ChatChannel`의 이름이나 `members`는 못바꿉니다.
        body의 `name`은 설명을 바꿀 `ChatChannel`의 이름입니다.
        `admins`안에 포함되지 않은 유저는 401이 나옵니다.
        """
        chat_channel = self.get_queryset().get(name__exact=request.data.get('name', None))

        if request.user not in chat_channel.admins.all():
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        chat_channel.description = request.data.get('description', None)
        chat_channel.save()

        serializer = ChatChannelSerializer(chat_channel)
        return Response(serializer.data)


class ChatChannelUpdateDeleteView(generics.UpdateAPIView,
                                  generics.DestroyAPIView):
    queryset = ChatChannel.objects.all()
    http_method_names = ['patch', 'delete']
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatChannelSerializer

    def get_queryset(self):
        hashed_value = self.kwargs.get('workspace__hashed_value', None)
        channel_name = self.kwargs.get('channel_name', None)
        result = self.queryset.get(workspace__hashed_value=hashed_value, name__exact=channel_name)
        return result

    def delete(self, request: Request, *args, **kwargs):
        chat_channel = self.get_queryset()

        if request.user not in chat_channel.admins.all():
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        chat_channel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(operation_id="channel_name_update")
    def patch(self, request: Request, *args, **kwargs):
        """
        `ChatChannel`의 이름을 바꿀때 사용합니다.
        path에 `channel_name`은 대상의 이름, body에 `name`은 새로 바꿀 이름입니다.
        """
        chat_channel: ChatChannel = self.get_queryset()

        if request.user not in chat_channel.admins.all():
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        chat_channel.name = request.data.get('name', None)
        chat_channel.save()
        serializer = self.get_serializer(chat_channel)
        return Response(serializer.data)


class ChatChannelAddMembersView(generics.CreateAPIView):
    queryset = ChatChannel.objects.all()
    http_method_names = ['post']
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatChannelMembersModifyRequestSerializer

    def get_queryset(self):
        hashed_value = self.kwargs.get('workspace__hashed_value', None)
        channel_name = self.kwargs.get('channel_name', None)
        result = self.queryset.get(workspace__hashed_value=hashed_value, name__exact=channel_name)
        return result

    def post(self, request: Request, *args, **kwargs):
        """
        채널에 인원을 추가 하고 싶을 때 쓰는 엔드포인트 입니다.
        배열을 쓰면 여러명을 추가 할 수 있습니다.
        `admins`에 포함되지 않은 유저는 401이 반환 됩니다.
        """
        chat_channel: ChatChannel = self.get_queryset()
        users = []
        try:
            for user in request.data.get('members_usernames', None):
                username = user.get("username", None)
                users.append(CustomUser.objects.get(username__exact=username))
        except CustomUser.DoesNotExist as e:
            return Response({'msg': str(e)}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in chat_channel.admins.all():
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        chat_channel.members.add(*users)
        chat_channel.save()

        serializer = ChatChannelSerializer(chat_channel)
        return Response(serializer.data)


class ChatChannelDeleteMembersView(generics.DestroyAPIView):
    queryset = ChatChannel.objects.all()
    http_method_names = ['delete']
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatChannelMembersModifyRequestSerializer

    def get_queryset(self):
        hashed_value = self.kwargs.get('workspace__hashed_value', None)
        channel_name = self.kwargs.get('channel_name', None)
        result = self.queryset.get(workspace__hashed_value=hashed_value, name__exact=channel_name)
        return result

    def delete(self, request: Request, *args, **kwargs):
        """
        특정 유저를 삭제 할 때 쓰는 엔드포인트 입니다.
        한번에 한명만 없앨 수 있습니다.
        `admins`에 없는 유저는 401을 반환 합니다. (특정 유저를 없앨 수 없습니다.)
        """
        username = kwargs.get('username', None)
        user = get_object_or_404(CustomUser, username__exact=username)

        chat_channel: ChatChannel = self.get_queryset()

        if request.user not in chat_channel.admins.all():
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        chat_channel.members.remove(user)
        chat_channel.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ChatChannelAddAdminsView(generics.CreateAPIView):
    queryset = ChatChannel.objects.all()
    http_method_names = ['post']
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatChannelAdminsModifyRequestSerializer

    def get_queryset(self):
        hashed_value = self.kwargs.get('workspace__hashed_value', None)
        channel_name = self.kwargs.get('channel_name', None)
        result = self.queryset.get(workspace__hashed_value=hashed_value, name__exact=channel_name)
        return result

    @swagger_auto_schema(responses={
        201: openapi.Response('response description', ChatChannelSerializer)
    })
    def post(self, request: Request, *args, **kwargs):
        """
        채널에 관리자를 추가 할 때 쓰는 엔드포인트 입니다.
        기존에 `admins`에 포함 되지 않은 유저는 추가 할 수 없고, 401이 반환 됩니다.
        """
        chat_channel: ChatChannel = self.get_queryset()
        users = []
        try:
            for user in request.data.get('admins_usernames', None):
                username = user.get("username", None)
                users.append(CustomUser.objects.get(username__exact=username))
        except CustomUser.DoesNotExist as e:
            return Response({'msg': str(e)}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in chat_channel.admins.all():
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        chat_channel.admins.add(*users)
        chat_channel.save()

        serializer = ChatChannelSerializer(chat_channel)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChatChannelDeleteAdminsView(generics.DestroyAPIView):
    queryset = ChatChannel.objects.all()
    http_method_names = ['delete']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        hashed_value = self.kwargs.get('workspace__hashed_value', None)
        channel_name = self.kwargs.get('channel_name', None)
        result = self.queryset.get(workspace__hashed_value=hashed_value, name__exact=channel_name)
        return result

    def delete(self, request: Request, *args, **kwargs):
        """
        관리자(`admins`)에서 특정 유저를 삭제 할 때 쓰는 엔드포인트 입니다.
        한번에 한명만 없앨 수 있습니다.
        `admins`에 없는 유저는 401을 반환 합니다. (특정 유저를 없앨 수 없습니다.)
        """
        username = kwargs.get('username', None)
        user = get_object_or_404(CustomUser, username__exact=username)

        chat_channel: ChatChannel = self.get_queryset()

        if request.user not in chat_channel.admins.all():
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        chat_channel.admins.remove(user)
        chat_channel.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
