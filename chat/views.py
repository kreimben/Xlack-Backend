from django.db.models import Prefetch
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response

from chat.models import Chat, ChatBookmark
from chat.serializers import ChatSerializer, ChatBookmarkSerializer
from chat_reaction.models import ChatReaction
from chat_reaction.serializers import ChatReactionListSerializer
from custom_user.models import CustomUser


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
        return self.queryset \
            .select_related('file', 'chatter', 'channel') \
            .filter(channel__hashed_value__exact=chv) \
            .prefetch_related(
            Prefetch(
                'bookmarks',
                queryset=ChatBookmark.objects.filter(chat__channel__hashed_value__exact=chv)
            ),
            Prefetch(
                'reaction',
                queryset=(ChatReaction.objects.filter(chat__channel__hashed_value__exact=chv)
                          .select_related('chat')
                          .prefetch_related(Prefetch('reactors',
                                                     queryset=CustomUser.objects.all())
                                            )
                          )
            )
        )

    def get(self, request: Request, *args, **kwargs):
        """
        url query에 `limit`, `offset`을 넣지 않으면 전체 값으로 일반 배열 형태로 결과가 나오고,
        넣었다면 아래 문서와 같이 results에 배열로 값이 들어갑니다.
        `has_bookmarked` field는 오직 "내가 북마크 했는지"만 표시됨으로, true 혹은 false값이 나옵니다.
        """
        q = self.get_queryset()
        q = list(q)  # For evaluating of queryset. If not to do this now, Redundant query will be executed.
        if page := self.paginate_queryset(q):
            q = page
        s = self.get_serializer(q, many=True)

        data = s.data[:]
        for i, chat in enumerate(q):
            d = data[i]

            for bookmark in chat.bookmarks.all():  # bookmarks:
                if bookmark.chat_id == d['id']:
                    d['has_bookmarked'] = True
                    break
            else:
                d['has_bookmarked'] = False

        if page is not None:
            return self.get_paginated_response(data)
        else:
            return Response(data)


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
