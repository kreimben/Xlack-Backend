from rest_framework import permissions, generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response

from chat.models import Chat
from chat.serializers import ChatSerializer


class ChatView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatSerializer
    pagination_class = LimitOffsetPagination
    lookup_field = 'channel_id'
    queryset = Chat.objects.order_by('-id').all()

    def list(self, request: Request, *args, **kwargs):
        channel_id = kwargs.get('channel_id', 1)

        limit = request.query_params.get('limit')
        offset = request.query_params.get('offset')

        p = LimitOffsetPagination()
        p.limit = limit
        p.offset = offset

        chats = Chat.objects.order_by('-id').filter(channel_id=channel_id)
        chats = p.paginate_queryset(chats, request)

        s = [ChatSerializer(chat) for chat in chats]

        return Response([chat.data for chat in s])
