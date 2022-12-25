from django.urls import path

from chat_channel import views

urlpatterns = [
    path('<str:workspace__hashed_value>/', views.ChatChannelView.as_view()),
    path('<str:workspace__hashed_value>/<str:channel_name>/', views.ChatChannelUpdateDeleteView.as_view()),
    path('<str:workspace__hashed_value>/<str:channel_name>/members/', views.ChatChannelAddMembersView.as_view()),
    path('<str:workspace__hashed_value>/<str:channel_name>/members/<str:username>/', views.ChatChannelDeleteMembersView.as_view()),
    path('<str:workspace__hashed_value>/<str:channel_name>/admins/', views.ChatChannelAddAdminsView.as_view()),
    path('<str:workspace__hashed_value>/<str:channel_name>/admins/<str:username>/', views.ChatChannelDeleteAdminsView.as_view())
]
