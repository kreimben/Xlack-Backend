import os

from dj_rest_auth.registration.views import SocialAccountListView
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Xlack",
        default_version="2.0.0",
        description="Xlack Backend API Documentation.",
        contact=openapi.Contact(email="aksidion@kreimben.com"),
        license=openapi.License(name="MIT"),
    ),
    url='https://api.xlack.kreimben.com/docs/' if not os.getenv('DJANGO_DEBUG') else 'http://127.0.0.1:8000/docs/',
    public=False,
    permission_classes=[permissions.IsAuthenticated],
)

urlpatterns = [
    path(f"{os.getenv('DJANGO_REAL_ADMIN_URI')}", admin.site.urls),
    # For OAuth2 Login and Registrations.
    path("accounts/", include("dj_rest_auth.urls")),
    path("token/", include("oauth2_token.urls")),
    path("socialaccounts/", SocialAccountListView.as_view(), name="socialaccount_connections"),
    # Swagger Documentation.
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger_documentation",
    ),
    path("channel/", include("chat_channel.urls")),
    path("workspace/", include("workspace.urls")),
    path("chat/", include("chat.urls")),
    path("profile/", include("user_profile.urls")),
    path("status/", include("status.urls")),
    path("file/", include("file.urls")),
    path("notifications/", include("notifications.urls")),
]
