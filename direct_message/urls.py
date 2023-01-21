from django.urls import path

from direct_message import views

urlpatterns = [
    path('<str:workspace__hashed_value>/', views.DMView.as_view()),
    path('<str:workspace__hashed_value>/<str:channel__hashed_value>/', views.DMDeleteView.as_view())
]
