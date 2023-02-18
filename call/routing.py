from django.urls import re_path

from call import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/call/$",
        consumers.CallConsumer.as_asgi()
    ),
]
