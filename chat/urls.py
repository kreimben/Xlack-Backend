from django.urls import path

from chat import views

urlpatterns = [
    path('<int:channel_id>/', views.ChatView.as_view())
]
