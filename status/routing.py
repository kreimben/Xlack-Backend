from django.urls import re_path

from status import consumers

websocket_urlpatterns = [
    re_path(r'ws/status/(?P<workspace_hashed_value>\w+)/$', consumers.StatusConsumer.as_asgi()),
]
