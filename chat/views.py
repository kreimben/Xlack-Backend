from rest_framework import generics, status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response

from chat.models import Chat, ChatBookmark, ChatReaction
from chat.serializers import ChatReactionSerializer, ChatSerializer, ChatBookmarkSerializer

from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_NUMBER, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema


class ChatView(generics.ListAPIView):
    """
    count는 전체 레코드의 수
    next, previous는 이전, 이후의 url
    """
    serializer_class = ChatSerializer
    pagination_class = LimitOffsetPagination
    queryset = Chat.objects.all()

    def get_queryset(self):
        chv = self.kwargs.get('channel__hashed_value', None)
        return self.queryset.filter(channel__hashed_value__exact=chv).order_by('-id')

    def get(self, request: Request, *args, **kwargs):
        """
        url query에 `limit`, `offset`을 넣지 않으면 전체 값으로 일반 배열 형태로 결과가 나오고,
        넣었다면 아래 문서와 같이 results에 배열로 값이 들어갑니다.
        `has_bookmarked` field는 오직 "내가 북마크 했는지"만 표시됨으로, true 혹은 false값이 나옵니다.
        """
        q = self.get_queryset()
        page = self.paginate_queryset(q)
        if page is not None:
            s = self.get_serializer(page, many=True)
            return self.get_paginated_response(s.data)
        else:
            s = self.get_serializer(q, many=True)
            for data in s.data[:]:
                try:
                    b = ChatBookmark.objects.get(
                        issuer=self.request.user, chat_id=data['id'])
                except ChatBookmark.DoesNotExist:
                    b = None
                data['has_bookmarked'] = True if b is not None else False
            return Response(s.data)


class ChatBookmarkCreateView(generics.CreateAPIView):
    queryset = ChatBookmark.objects.all()
    serializer_class = ChatBookmarkSerializer

    def post(self, request: Request, *args, **kwargs):
        s = self.get_serializer(data=request.data)
        if s.is_valid():
            chat_id = s.data.get('chat_id')
            chat_bookmark, is_created = ChatBookmark.objects.get_or_create(
                issuer=request.user, chat_id=chat_id)
            s = self.get_serializer(chat_bookmark)
            return Response(s.data)
        else:
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatBookmarkDeleteView(generics.DestroyAPIView):
    queryset = ChatBookmark.objects.all()
    serializer_class = ChatBookmarkSerializer

    def delete(self, request: Request, *args, **kwargs):
        chat_id = kwargs.get('chat_id', None)
        chat_bookmark = get_object_or_404(
            ChatBookmark, issuer=request.user, chat_id=chat_id)
        chat_bookmark.delete()
        return Response(status=status.HTTP_302_FOUND)


@swagger_auto_schema(
    request_body=Schema(
        type=TYPE_OBJECT,
        properties={
            "chat_id": Schema(type=TYPE_NUMBER, description="id_of_chat"),
            "icon": Schema(
                type=TYPE_STRING, description="icon of reaction"
            ),
        },
    )
)
class ChatReactionCreateView(generics.CreateAPIView):
    """ Endpoint for creating new reaction or
        adding user to existing reaction
        (Debug use only)
    """
    queryset = ChatReaction.objects.all()
    http_method_names = ['post']
    serializer_class = ChatReactionSerializer

    def post(self, request: Request, *args, **kwargs):
        serial = self.get_serializer(data=request.data)
        if serial.is_valid():
            chat = serial.data.get('chat_id')
            icon = serial.data.get('icon')

            reaction, is_created = ChatReaction.objects.get_or_create(
                chat_id=chat, icon=icon)

            if request.user not in reaction.reactors.all():
                reaction.reactors.add(request.user)
                serial = self.get_serializer(reaction)
                return Response(serial.data)
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    request_body=Schema(
        type=TYPE_OBJECT,
        properties={
            "chat_id": Schema(type=TYPE_NUMBER, description="id_of_chat"),
            "icon": Schema(
                type=TYPE_STRING, description="icon_of_reaction"
            ),
        },
    )
)
class ChatReactionRemoveView(generics.DestroyAPIView):
    """ Endpoint for removing user to existing reaction
        (Debug use only)
    """
    queryset = ChatReaction.objects.all()
    http_method_names = ['delete']
    serializer_class = ChatReactionSerializer

    def delete(self, request: Request, *args, **kwargs):

        serial = self.get_serializer(data=request.data)

        if serial.is_valid():
            chat = serial.data.get('chat_id')
            icon = serial.data.get('icon')

            reaction = ChatReaction.objects.get(chat_id=chat, icon=icon)

            if request.user not in reaction.reactors.all():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                reaction.reactors.remove(request.user)
                if reaction.reactors.count() == 0:
                    reaction.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    serial = self.get_serializer(reaction)
                    return Response(serial.data)

        else:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
