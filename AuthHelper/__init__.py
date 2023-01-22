from rest_framework_simplejwt.tokens import AccessToken

from custom_user.models import CustomUser


class AuthHelper:

    @classmethod
    def find_user_by_access_token(cls, access_token: str) -> (CustomUser, int):
        """
        find user by access token.
        access_token: put access token
        return: `CustomUser` object and user pk.
        """

        access_token_obj = AccessToken(access_token)
        user_id = access_token_obj['user_id']
        user = CustomUser.objects.get(id=user_id)
        return user, user_id
