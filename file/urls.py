from rest_framework.routers import DefaultRouter

from file.views import FileViewSet

router = DefaultRouter()

router.register('', FileViewSet)

urlpatterns = router.urls
