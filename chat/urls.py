from rest_framework import routers

from chat import views

router = routers.DefaultRouter()

router.register('', views.ChatViewSet)

urlpatterns = router.urls
