import base64
import json
import logging
import os
from datetime import timedelta

from fastapi import APIRouter, Request, Query, Depends, Body
from jwt import decode, ExpiredSignatureError
from sqlalchemy.orm import Session
from starlette import status

from ..model.crud.user import read_user
from ..model.crud.user_tokens import update_user_tokens, read_user_tokens
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
    return SuccessResponse(url=url)


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

    return get_user_info(access_token)
    # return SuccessResponse(message='Successfully get access token from github.', access_token=access_token)


@router.get('/user_info/github', deprecated=True)
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
async def update_access_token(refresh_token: str = Body(...),
                              db: Session = Depends(get_db)):
    # Check whether access token is expired first.
    try:
        decode(refresh_token, key='secret_key', algorithms=['HS256'])
        return FailureResponse(message='You can this endpoint when only access token is expired.',
                               status_code=status.HTTP_403_FORBIDDEN)
    except ExpiredSignatureError:
        # Surely, If the token is not expired, No reason to proceeds this function (logic).
        pass

    # Get payload from expired token.
    payload = refresh_token.split(".")[1]
    padded = payload + "=" * (4 - len(payload) % 4)
    decoded = base64.b64decode(padded)
    payload = json.loads(decoded)

    # Issue a new thing.
    user = await read_user(db=db, user_id=payload['user_id'])
    token = issue_token(user_info=user.to_dict(), delta=timedelta(hours=1))

    # await update_user_tokens(db=db, user_id=user.user_id, new_refresh_token=token)
    return SuccessResponse(message='Successfully re-issued refresh token', token=token)


@router.get('/user_check')
async def check_user_by_github_id(github_id: int,
                                  db: Session = Depends(get_db)):
    user = await read_user(db=db, github_id=github_id)
    if user:
        return SuccessResponse(message='User exists. You don\'t need to register.', status_code=status.HTTP_200_OK)
    else:
        return FailureResponse(message='User doesn\'t exists. You have to register.',
                               status_code=status.HTTP_404_NOT_FOUND)


@router.post('/issue_tokens')
async def issue_tokens(github_id: int,
                       db: Session = Depends(get_db)):
    user = await read_user(db=db, github_id=github_id)
    if user:
        token_info = await read_user_tokens(db=db, user_id=user.user_id)
        access_token = issue_token(user.to_dict(), timedelta(hours=1))
        refresh_token = token_info.refresh_token
        return SuccessResponse(message='Successfully get new tokens',
                               access_token=access_token,
                               refresh_token=refresh_token)
    else:
        return FailureResponse(message='User doesn\'t exists. You have to register.',
                               status_code=status.HTTP_404_NOT_FOUND)
