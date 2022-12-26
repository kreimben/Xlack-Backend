# notifications/utils.py

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from django.contrib.auth.models import User

import asyncio

"""
utils like verifying, finding
and check status
"""

# forked from status.consumer


def find_user(access_token: str) -> tuple(User | None, int | None):
    try:
        access_token_obj = AccessToken(access_token)
    except TokenError:
        return None, None
    user_id = access_token_obj["user_id"]
    user = User.objects.get(id=user_id)

    return user, user_id


def find_access_token(scope) -> str | None:
    access_token = None
    for element in scope["headers"]:
        if element[0] == b"authorization" or element[0] == b"Authorization":
            access_token = element[1]

    return access_token.split()[1]


async def delay(delay, func, **kwargs):
    await asyncio.sleep(delay)
    func(kwargs)
