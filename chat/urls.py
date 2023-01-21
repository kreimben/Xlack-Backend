from django.urls import path

from chat import views

from chat_reaction.views import ChatReactionView

urlpatterns = [
    path('bookmark/', views.ChatBookmarkCreateView.as_view()),
    path('bookmark/<int:chat_id>/', views.ChatBookmarkDeleteView.as_view()),
    path('reaction/', ChatReactionView.as_view()),
    path('<str:channel__hashed_value>/', views.ChatView.as_view()),
]
