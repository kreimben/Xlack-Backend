from django.urls import path, include
from rest_framework import routers

from chat_channel import views

router = routers.DefaultRouter()

router.register('', views.ChatChannelViewSet)

urlpatterns = router.urls