from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from ..model.crud import user, authorization
from ..utils.github_auth import exchange_code_for_access_token, get_user_data_from_github
import os

router = APIRouter(prefix='/auth', tags=['auth'])


@router.get('/login')
async def login_github():
    client_id = os.getenv('GITHUB_CLIENT_ID')
    # redirect_uri = 'https://xlack.kreimben.com/auth/redirect/github'
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

    access_token = res.content.split('&').split('=')[1]
    print(f'access_token: {access_token}')

    return {
        'success': True,
        'message': res
    }


@router.get('/user_info')
async def get_user_info(access_token: str):
    res = get_user_data_from_github(access_token)
    return {
        'success': True,
        'message': res
    }
