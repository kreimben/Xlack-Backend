from django.urls import path

from .views import CounterView

urlpatterns = [
    path("<str:channel__hashed_value>/", CounterView.as_view()),
]
