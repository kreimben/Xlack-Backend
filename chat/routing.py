from django.urls import path

from chat import consumers

urlpatterns = [
    path('ws/chat/<str:channel_id>/', consumers.ChatConsumer.as_asgi()),
]
