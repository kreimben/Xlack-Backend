import deprecated
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from custom_user.models import CustomUser


@deprecated.deprecated('No reason to use this exception.')
class AccessTokenNotIncludedInHeader(Exception):
    def __init__(self, *args, **kwargs):
        super(*args, **kwargs)


class AuthHelper:
    @classmethod
    @deprecated.deprecated('No reason to use this method.')
    def find_user(cls, scope) -> CustomUser | None:
        """
        To find user object in consumer with `scope` directly.
        """
        access_token = cls.find_access_token(scope)
        if access_token is None:
            print('Authorization token not found!')
            raise AccessTokenNotIncludedInHeader

        user, pk = cls.find_user_by_access_token(access_token)
        return user

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

    @classmethod
    @deprecated.deprecated('There is no way to find access token with header in websocket.')
    def find_access_token(cls, scope) -> str | None:
        access_token = None
        for element in scope["headers"]:
            if element[0] == b'authorization' or element[0] == b'Authorization':
                access_token = element[1]
                break
        else:
            return None

        return access_token.split()[1]
