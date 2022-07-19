import logging
import os

import requests


def exchange_code_for_access_token(code: str, redirect_uri: str | None = None):
    logging.debug(f'in exchange_code_for_access_token (github_auth.py)')
    params = {
        'client_id': os.getenv('GITHUB_CLIENT_ID'),
        'client_secret': os.getenv('GITHUB_CLIENT_SECRET'),
        'code': code
    }

    if redirect_uri is not None:
        params.update({'redirect_uri': redirect_uri})

    logging.debug(f'params: {params}')

    res = requests.post('https://github.com/login/oauth/access_token', params=params)
    logging.debug(f'res: {res}')

    return res


def get_user_data_from_github(access_token: str):
    logging.debug(f'in get_user_data_from_github (github_auth.py)')
    res = requests.get('https://api.github.com/user', headers={
        'Authorization': f'token {access_token}'
    })
    logging.debug(f'res: {res}')
    return res
