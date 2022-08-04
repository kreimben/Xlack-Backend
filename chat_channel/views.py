from rest_framework import viewsets

from chat_channel.models import ChatChannel
from chat_channel.serializers import ChatChannelSerializer


class ChatChannelViewSet(viewsets.ModelViewSet):
    queryset = ChatChannel.objects.order_by('name').all()
    serializer_class = ChatChannelSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
