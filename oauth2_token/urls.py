from django.urls import path

from oauth2_token.views import GithubLoginView, GithubConnect

urlpatterns = [
    path('github/', GithubLoginView.as_view(), name='github_login'),
    path('github/connect/', GithubConnect.as_view(), name='github_connect'),
]
