from django.urls import path

from status.views import UserStatusView

urlpatterns = [
    path('<str:workspace_hashed_value>/', UserStatusView.as_view())
]