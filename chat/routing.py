from django.urls import re_path

from chat import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_channel_hashed_value>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
