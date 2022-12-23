from django.urls import path

from chat_channel import views

urlpatterns = [
    path('<str:workspace__hashed_value>/', views.ChatChannelView.as_view()),
    path('<str:workspace__hashed_value>/<str:channel_name>/', views.ChatChannelUpdateDeleteView.as_view())
]
