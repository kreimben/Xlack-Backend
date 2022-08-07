from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from chat.models import Chat
from chat.serializers import ChatSerializer


class ChatViewSet(ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    http_method_names = ['get']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
