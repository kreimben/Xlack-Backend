from rest_framework import permissions, generics
from rest_framework.pagination import LimitOffsetPagination

from chat.models import Chat
from chat.serializers import ChatSerializer


class ChatView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatSerializer
    pagination_class = LimitOffsetPagination
    lookup_field = 'channel_id'
    queryset = Chat.objects.order_by('-id').all()
