from django.urls import path

from search.views import SearchView

urlpatterns = [
    path('<str:search_keyword>/', SearchView.as_view()),
]