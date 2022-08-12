from rest_framework.routers import DefaultRouter

from user_profile import views

router = DefaultRouter()

router.register('', views.UserProfileViewSet, basename='UserProfile')

urlpatterns = router.urls
