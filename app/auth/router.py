from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from ..model.crud import user, authorization
from ..utils.github_auth import exchange_code_for_access_token, get_user_data_from_github

router = APIRouter(prefix='/auth', tags=['auth'])


@router.get('/login')
async def login_github():
    return RedirectResponse(
        'https://github.com/login/oauth/authorize?client_id=9ac10cd868488ad0185b&redirect_uri=127.0.0.1:8080/redirect/github&scope=read:user')


@router.get('/redirect/github')
async def redirect_github(request: Request):
    """
    This function deal with after redirect from client.

    :return:
    """

    print(f'params: {request.query_params}')

    res = exchange_code_for_access_token('sdf')

    print(f'res: {res}')

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
