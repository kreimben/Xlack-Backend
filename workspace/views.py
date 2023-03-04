from uuid import uuid4

from django.db.models import Prefetch
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.openapi import TYPE_OBJECT, TYPE_STRING, Schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response

from chat.models import Chat
from chat.serializers import BookmarkedChatsSerializer
from chat_channel.models import ChatChannel
from workspace.models import Workspace
from workspace.serializers import BaseWorkspaceSerializer, NameWorkspaceSerializer


class WorkspaceView(
    generics.CreateAPIView,
    generics.ListAPIView,
    generics.UpdateAPIView,
    generics.DestroyAPIView,
):
    serializer_class = NameWorkspaceSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]

    @swagger_auto_schema()
    def post(self, request: Request, *args, **kwargs):
        name = request.data.get("name", None)

        if not name:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        s: NameWorkspaceSerializer = self.get_serializer(
            data=request.data, context=request
        )

        if s.is_valid():
            # 파이썬 랜덤 uuid값은 8자리 수 뒤에 -가 한글자 나와서 8자까지만 사용.
            workspace: Workspace = s.save(hashed_value=str(uuid4())[:8])
            workspace.members.add(request.user)
            workspace.save()
            s = self.get_serializer(workspace)
            return Response(status=status.HTTP_200_OK, data=s.data)
        else:
            return JsonResponse(
                status=status.HTTP_400_BAD_REQUEST, data={"msg": s.errors}
            )

    def get(self, request: Request, *args, **kwargs):
        """
        자신이 가입한 workspace만 배열로 나옵니다.
        """
        workspaces = request.user.joined_workspaces.all()
        s = self.get_serializer(workspaces, many=True)
        return Response(s.data)

    @swagger_auto_schema(
        request_body=Schema(
            type=TYPE_OBJECT,
            properties={
                "old_name": Schema(type=TYPE_STRING, description="string"),
                "new_name": Schema(type=TYPE_STRING, description="string"),
            },
        )
    )
    def patch(self, request: Request, *args, **kwargs):
        """
        workspace의 이름을 바꾸는 엔드포인트 입니다.
        workspace에 가입하려면 다른 엔드포인트를 사용하십시오.
        """
        old_name = request.data.get("old_name", None)
        new_name = request.data.get("new_name", None)

        if not old_name or not new_name:
            return JsonResponse(
                status=status.HTTP_400_BAD_REQUEST,
                data={"msg": "fill old_name and new_name both."},
            )

        try:
            workspace = Workspace.objects.get(name__exact=old_name)
            workspace.name = new_name
            workspace.save()

            s = BaseWorkspaceSerializer(workspace, context=request)
            return Response(status=status.HTTP_200_OK, data=s.data)
        except Workspace.DoesNotExist as e:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, data={"msg": str(e)})

    @swagger_auto_schema(
        request_body=Schema(
            type=TYPE_OBJECT,
            properties={
                "name": Schema(type=TYPE_STRING, description="string"),
                "hashed_value": Schema(type=TYPE_STRING, description="string"),
            },
        )
    )
    def delete(self, request: Request, *args, **kwargs):
        """
        body에 `name`과 `hased_value` 둘 중에 하나 넣으면 됩니다.
        """
        name = request.data.get("name", None)
        hashed_value = request.data.get("hashed_value", None)

        try:
            if name:
                workspace = Workspace.objects.get(name__exact=name)
            elif hashed_value:
                workspace = Workspace.objects.get(hashed_value__exact=hashed_value)
            else:
                return JsonResponse(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"msg": "please input name or hashed_value"},
                )

            workspace.delete()
            return Response(status=status.HTTP_200_OK)
        except Workspace.DoesNotExist as e:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, data={"msg": str(e)})


class WorkspaceBookmarkedChatView(generics.ListAPIView):
    serializer_class = NameWorkspaceSerializer
    http_method_names = ['get']
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        # Get workspace hashed value.
        # Filter chat using workspace hashed value and That I bookmarked.
        whv = self.kwargs.get('workspace_hashed_value')
        chats = Chat.objects \
            .select_related('chatter', 'file') \
            .prefetch_related('bookmarks', 'reaction') \
            .filter(channel__workspace__hashed_value__exact=whv, bookmarks__issuer=self.request.user.id) \
            .order_by('-created_at')
        return chats

    @swagger_auto_schema(
        responses={200: openapi.Response('내가 북마크한 채팅만 리스트로 보내줍니다.', BookmarkedChatsSerializer(many=True))})
    def get(self, request, *args, **kwargs):
        q = self.get_queryset()

        if page := self.paginate_queryset(q):
            q = page
        s = BookmarkedChatsSerializer(q, many=True)

        if page is not None:
            return self.get_paginated_response(s.data)
        else:
            return Response(s.data)
