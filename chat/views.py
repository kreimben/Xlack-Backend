from rest_framework import permissions, generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response

from chat.models import Chat, ChatBookmark
from chat.serializers import ChatSerializer, ChatBookmarkSerializer


class ChatView(generics.ListAPIView):
    """
    count는 전체 레코드의 수
    next, previous는 이전, 이후의 url
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatSerializer
    pagination_class = LimitOffsetPagination
    lookup_field = 'channel_id'
    queryset = Chat.objects.order_by('-id').all()

    def get_queryset(self):
        cid = self.kwargs['channel_id']
        return self.queryset.filter(channel_id=cid)


class ChatBookmarkCreateView(generics.CreateAPIView):
    queryset = ChatBookmark.objects.all()
    serializer_class = ChatBookmarkSerializer

    def post(self, request: Request, *args, **kwargs):
        s = self.get_serializer(data=request.data)
        if s.is_valid():
            chat_id = s.data.get('chat_id')
            chat_bookmark, is_created = ChatBookmark.objects.get_or_create(issuer=request.user, chat_id=chat_id)
            s = self.get_serializer(chat_bookmark)
            return Response(s.data)
        else:
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatBookmarkDeleteView(generics.DestroyAPIView):
    queryset = ChatBookmark.objects.all()
    serializer_class = ChatBookmarkSerializer

    def delete(self, request: Request, *args, **kwargs):
        chat_id = kwargs.get('chat_id', None)
        chat_bookmark = get_object_or_404(ChatBookmark, issuer=request.user, chat_id=chat_id)
        print(f'{chat_bookmark=}')
        chat_bookmark.delete()
        return Response(status=status.HTTP_302_FOUND)
