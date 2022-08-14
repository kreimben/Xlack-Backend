import os

from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView, SocialConnectView


class GithubLoginView(SocialLoginView):
    """
    오직 code에만 값을 넣고 다른 것은 그냥 ""처리 하시면 됩니다.
    """
    adapter_class = GitHubOAuth2Adapter
    client_class = OAuth2Client
    callback_url = os.getenv('GITHUB_LOGIN_CALLBACK')


class GithubConnect(SocialConnectView):
    """
    일반적으로 사용할 필요가 없는 엔드포인트 입니다.
    기존에 장고 어드민 아이디가 있는 유저가 github로그인 연동을 하고 싶을때 사용하면 됩니다.
    email을 중심으로 작동함으로 장고 어드민 계정에 설정해둔 email과 깃헙에서 설정해둔 이메일이 다르다면
    계정 통합이 되지 않습니다.
    """
    adapter_class = GitHubOAuth2Adapter
    client_class = OAuth2Client
    callback_url = os.getenv('GITHUB_LOGIN_CALLBACK')
