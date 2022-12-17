from rest_framework import permissions, generics
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from chat.models import Chat
from chat.serializers import ChatSerializer


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
