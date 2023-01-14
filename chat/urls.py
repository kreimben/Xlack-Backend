from django.urls import path

from chat import views

urlpatterns = [
    path('bookmark/', views.ChatBookmarkCreateView.as_view()),
    path('bookmark/<int:chat_id>/', views.ChatBookmarkDeleteView.as_view()),
    path('<str:channel__hashed_value>/', views.ChatView.as_view()),
    path('reaction/', views.ChatReactionCreateView.as_view()),
    path('reaction/remove/', views.ChatReactionRemoveView.as_view())
]
