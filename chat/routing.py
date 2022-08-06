from django.template.defaulttags import url

from chat import consumers

websocket_urlpatterns = [
    # path('/chat/<str:channel_id>/', consumers.ChatConsumer.as_asgi())
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer)
]
