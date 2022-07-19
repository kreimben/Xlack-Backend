import base64
import json
import logging
import os
from datetime import timedelta

from fastapi import APIRouter, Request, Query, Depends, Body
from fastapi.responses import RedirectResponse
from jwt import decode, ExpiredSignatureError
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from ..errors.jwt_error import AccessTokenExpired
from ..model.crud.user_tokens import update_user_tokens
from ..model.crud.user import update_user, read_user
from ..model.database import get_db
from ..utils.github_auth import exchange_code_for_access_token, get_user_data_from_github
from ..utils.jwt import issue_token
from ..utils.responses import FailureResponse, SuccessResponse

router = APIRouter(prefix='/authentication', tags=['authentication'])


@router.get('/github_login')
async def login_github():
    """
    Get redirect response to GitHub OAuth2.
    Test code for testing backend redirect codes.
    Frontend team may not use this endpoint.

    :return:
    """
    logging.info('GET /authentication/github_login')

    client_id = os.getenv('GITHUB_CLIENT_ID')
    scope = 'read:user'
    url = f'https://github.com/login/oauth/authorize?client_id={client_id}&scope={scope}'
    logging.debug(f'url: {url}')
    return RedirectResponse(url)


@router.get('/redirect/github')
async def redirect_github(request: Request, code: str):
    """
    This function deal with after redirect from client.

    :return:
    """
    logging.info('GET /authentication/redirect/github')
    logging.debug(f'params: {request.query_params}')
    logging.debug(f'code: {code}')
    res = exchange_code_for_access_token(code)

    logging.debug(f'res: {res.content}')

    content = str(res.content)

    # Check error message.
    # I know it's really messy way to deal with, But that's my best.
    first_word = content.split('&')[0].split('=')[0]
    if first_word == 'b\'error':
        return FailureResponse(message=content.split('&')[1].split('=')[1])

    access_token = content.split('&')[0].split('=')[1]

    return SuccessResponse(message='Successfully get access token from github.', access_token=access_token)


@router.get('/user_info/github')
async def get_user_info(github_access_token: str = Query(
    alias='Access Token From Github.',
    title='github access token',
    description='You should input only GITHUB ACCESS TOKEN!!!',
    max_length=50,
    min_length=30)
):
    """
    When you get information from github directly using github access token.

    :param github_access_token:
    :return:
    """
    logging.info('GET /authentication/user_info/github')
    res = get_user_data_from_github(github_access_token)
    logging.debug(f'responses from github: {res}')
    return SuccessResponse(message='Successfully get user information from github.',
                           github_info=json.loads(res.content))


@router.post('/revoke_token/{user_id}')
async def revoke_token(user_id: int, db: Session = Depends(get_db)):
    logging.info('GET /authentication/revoke_token/{user_id}')
    user_info = await read_user(db, user_id=user_id)

    # Check `user_id` is valid first.
    if user_info is None:
        logging.info('No such user')
        return FailureResponse(message='No such user', status_code=status.HTTP_404_NOT_FOUND)

    rows = await update_user_tokens(db=db, user_id=user_id, new_refresh_token=None)
    if not rows:
        logging.warning('Not updated!')
        return FailureResponse(message='Not updated!', status_code=status.HTTP_404_NOT_FOUND)
    else:
        return SuccessResponse(message='Successfully revoked refresh token.')


@router.post('/update/access_token')
async def update_access_token(access_token: str = Body(...),
                              db: Session = Depends(get_db)):
    return await __issue_new_token(token=access_token, is_access_token=True, db=db)


@router.post('/update/refresh_token')
async def update_refresh_token(refresh_token: str = Body(...),
                               db: Session = Depends(get_db)):
    return await __issue_new_token(token=refresh_token, is_access_token=False, db=db)


async def __issue_new_token(token: str = Body(...),
                            is_access_token: bool = True,
                            db: Session = Depends(get_db)):
    """
    Helper function that helps common logic
    """

    # Check whether access token is expired first.
    try:
        decode(token, key='secret_key', algorithms=['HS256'])
        return FailureResponse(message='You can this endpoint when only access token is expired.',
                               status_code=status.HTTP_403_FORBIDDEN)
    except ExpiredSignatureError:
        pass

    # Get payload from expired token.
    payload = token.split(".")[1]
    padded = payload + "=" * (4 - len(payload) % 4)
    decoded = base64.b64decode(padded)
    payload = json.loads(decoded)
    print(f'payload: {payload}')

    # Issue a new thing.
    user = await read_user(db=db, user_id=payload['user_id'])
    payload = {
        'user_id': user.user_id,
        'email': user.email,
        'name': user.name,
        'authorization': user.authorization,
        'created_at': str(user.created_at),
        'thumbnail_url': user.thumbnail_url
    }  # This code is inevitable to convert to `dict` object. Fucking `datetime` is not json parsable.
    token = issue_token(user_info=payload, delta=timedelta(hours=1) if is_access_token else timedelta(days=14))

    if is_access_token:
        return SuccessResponse(message='Successfully re-issued access token.', token=token)
    else:  # in case refresh token
        await update_user_tokens(db=db, user_id=user.user_id, new_refresh_token=token)
        return SuccessResponse(message='Successfully re-issued refresh token', token=token)
