from django.urls import path

from chat_channel import views

urlpatterns = [
    path('<str:workspace__hashed_value>/', views.ChatChannelView.as_view()),
    path('<str:workspace__hashed_value>/<str:channel__hashed_value>/', views.ChatChannelUpdateDeleteView.as_view()),
    path('<str:workspace__hashed_value>/<str:channel__hashed_value>/members/', views.ChatChannelAddMembersView.as_view()),
    path('<str:workspace__hashed_value>/<str:channel__hashed_value>/members/<str:username>/', views.ChatChannelDeleteMembersView.as_view()),
    path('<str:workspace__hashed_value>/<str:channel__hashed_value>/admins/', views.ChatChannelAddAdminsView.as_view()),
    path('<str:workspace__hashed_value>/<str:channel__hashed_value>/admins/<str:username>/', views.ChatChannelDeleteAdminsView.as_view())
]
