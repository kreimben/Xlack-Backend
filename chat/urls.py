from django.urls import path

from chat import views

urlpatterns = [
    path('<int:channel_id>/', views.ChatView.as_view()),
    path('bookmark/', views.ChatBookmarkCreateView.as_view()),
    path('bookmark/<int:chat_id>/', views.ChatBookmarkDeleteView.as_view())
]
