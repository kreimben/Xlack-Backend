from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from ..model.crud import user, authorization
from ..utils.github_auth import exchange_code_for_access_token, get_user_data_from_github
import os

router = APIRouter(prefix='/auth', tags=['auth'])


@router.get('/login')
async def login_github():
    client_id = os.getenv('GITHUB_CLIENT_ID')
    scope = 'read:user'
    url = f'https://github.com/login/oauth/authorize?client_id={client_id}&scope={scope}'
    print(f'url: {url}')
    return RedirectResponse(url)


@router.get('/redirect/github')
async def redirect_github(request: Request, code: str):
    """
    This function deal with after redirect from client.

    :return:
    """

    print(f'params: {request.query_params}')
    print(f'code: {code}')
    res = exchange_code_for_access_token(code)

    print(f'res: {res.content}')

    content = str(res.content)

    first_word = content.split('&')[0].split('=')[0]

    if first_word == 'b\'error':
        return {
            'success': False,
            'message': 'Failed to get access token.',
            'detail': content.split('&')[1].split('=')[1]
        }

    access_token = content.split('&')[0].split('=')[1]

    return {
        'success': True,
        'message': 'Successfully get access token from github.',
        'access_token': access_token
    }


@router.get('/user_info')
async def get_user_info(access_token: str):
    res = get_user_data_from_github(access_token)
    return {
        'success': True,
        'message': res
    }
