import os
from json import JSONDecodeError

import requests


def exchange_code_for_access_token(code: str, redirect_uri: str | None = None):
    params = {
        'client_id': os.getenv('GITHUB_CLIENT_ID'),
        'client_secret': os.getenv('GITHUB_CLIENT_SECRET'),
        'code': code
    }

    if redirect_uri is not None:
        params.update({'redirect_uri': redirect_uri})

    res = requests.post('https://github.com/login/oauth/access_token', params=params)

    return res


def get_user_data_from_github(access_token: str):
    res = requests.get('https://api.github.com/user', auth=f'token {access_token}')
    return res.json()
