from django.urls import re_path

from chat_reaction import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/chat_reaction/(?P<chat_channel_hashed_value>\w+)/$",
        consumers.ReactionConsumer.as_asgi(),
    ),
]
