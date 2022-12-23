from django.urls import re_path

from notifications import consumers

websocket_urlpatterns = [
    re_path(
        # have to add point
        r"ws//(?\w+)/$",
        consumers.NotificationsConsumer.as_asgi(),
    ),
]
