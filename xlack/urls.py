"""xlack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Xlack",
        default_version='2.0.0',
        description="Xlack Backend API Documentation.",
        contact=openapi.Contact(email="aksidion@kreimben.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticated],
)

urlpatterns = [
    path(os.getenv('DJANGO_REAL_ADMIN_URI'), admin.site.urls),

    # Normal Login.
    path('accounts/', include('rest_framework.urls', namespace='rest_framework')),

    # For OAuth2 Login and Registrations.
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/', include('allauth.urls')),

    # Swagger Documentation.
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_documentation'),

    path('channel/', include('chat_channel.urls')),
    path('workspace/', include('workspace.urls')),
    path('chat/', include('chat.urls')),
    path('profile/', include('user_profile.urls')),
    # path('ws/chat/', include('chat.routing')),

    path('token/', include('oauth2_token.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
