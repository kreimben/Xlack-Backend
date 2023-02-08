"""
ASGI config for xlack project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xlack.settings")

import django

django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import chat.routing
import chat_reaction.routing
import status.routing
import notifications.routing
import call.routing

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
                + status.routing.websocket_urlpatterns
                + notifications.routing.websocket_urlpatterns
                + chat_reaction.routing.websocket_urlpatterns
                + call.routing.websocket_urlpatterns
            )
        ),
    }
)
