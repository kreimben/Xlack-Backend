from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

from chat_channel.models import ChatChannel
from chat_channel.serializers import ChatChannelSerializer
from custom_user.models import CustomUser
from direct_message.serializers import DMCreateSerializer
from workspace.models import Workspace


class DMDeleteView(generics.DestroyAPIView):
    queryset = ChatChannel.dm_objects.all()
    serializer_class = ChatChannelSerializer
    http_method_names = ['delete']

    def get_queryset(self):
        workspace_hashed_value = self.kwargs.get('workspace__hashed_value', None)
        channel_hashed_value = self.kwargs.get('channel__hashed_value', None)
        result = self.queryset.filter(workspace__hashed_value=workspace_hashed_value,
                                      hashed_value__exact=channel_hashed_value)
        return result

    def delete(self, request: Request, *args, **kwargs):
        """
        혹시 필요할지도 몰라서 만들긴 했는데 진짜 쓸 수 있는 곳이 있을지 모르겠다.
        """
        channel = self.get_queryset()
        channel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DMView(generics.CreateAPIView,
             generics.ListAPIView):
    queryset = ChatChannel.dm_objects.all()
    serializer_class = ChatChannelSerializer
    http_method_names = ['get', 'post']

    def get_queryset(self):
        hashed_value = self.kwargs.get('workspace__hashed_value', None)
        result = self.queryset.filter(workspace__hashed_value=hashed_value)
        return result

    def get(self, request: Request, *args, **kwargs):
        """
        "내가" 예전에 대화를 나눈 적이 있는 대상(채널이 만들어진 적이 있는 것들)만 나옵니다.
        """
        all_dm = []
        hashed_value = self.kwargs.get('workspace__hashed_value', None)
        for channel in request.user.chat_channel_members.all():
            if channel.is_dm and channel.workspace.hashed_value == hashed_value:
                all_dm.append(channel)
        s = self.get_serializer(all_dm, many=True)
        return Response(s.data)

    @swagger_auto_schema(request_body=DMCreateSerializer, responses={'201': ChatChannelSerializer})
    def post(self, request: Request, *args, **kwargs):
        """
        내가 DM을 만들고 싶은 대상의 user id를 넣으면 됩니다.
        """
        try:
            target_user = CustomUser.objects.get(pk=request.data.get('target_user_id', None))
        except CustomUser.DoesNotExist:
            return Response({'msg': f"No such user: {request.data.get('target_user_id', None)}"},
                            status=status.HTTP_404_NOT_FOUND)

        hashed_value = self.kwargs.get('workspace__hashed_value', None)
        workspace = Workspace.objects.get(hashed_value__exact=hashed_value)
        if target_user not in workspace.members.all():
            return Response({'msg': f'That user is not in wanted workspace!'}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.id < target_user.id:
            channel_name = f'dm-{request.user.id}-{target_user.id}'
        else:
            channel_name = f'dm-{target_user.id}-{request.user.id}'

        chat_channel, _ = ChatChannel.objects.get_or_create(name=channel_name,
                                                            workspace=workspace,
                                                            is_dm=True)
        chat_channel.members.add(request.user, target_user)
        chat_channel.admins.add(request.user, target_user)

        serializer = self.get_serializer(chat_channel)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
