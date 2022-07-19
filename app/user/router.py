import logging
from datetime import timedelta

import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Path
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..errors.jwt_error import RefreshTokenExpired, AccessTokenExpired
from ..model.crud import authorization
from ..model.crud.authorization import read_authorization
from ..model.crud.user_tokens import create_user_tokens, update_user_tokens, delete_user_tokens
from ..model.crud.user import read_users, read_user, update_user, delete_user, create_user
from ..model.database import get_db
from ..model.schemas import UserCreate, UserInformation
from ..utils.jwt import issue_token, check_auth_using_token
from ..utils.responses import FailureResponse, SuccessResponse

router = APIRouter(prefix='/user', tags=['user'])


@router.post('/')
async def user_create(user_info: UserCreate,
                      db: Session = Depends(get_db)):
    """
    Access token's expiration is 1 hour.
    Refresh token's expiration is 14 days.
    """
    logging.info('POST /user/')

    # Check authorization first!
    if not await authorization.read_authorization(name=user_info.authorization, db=db):
        logging.debug('No such authorization.')
        raise HTTPException(status_code=404, detail='No such authorization.')

    created_user = await create_user(github_id=str(user_info.github_id),
                                     email=user_info.email,
                                     name=user_info.name,
                                     authorization_name=user_info.authorization,
                                     thumbnail_url=user_info.thumbnail_url,
                                     db=db)
    logging.debug(f'user created: {created_user}')

    # user = await read_user(db=db, user_id=created_user.user_id)
    print(f'user: {created_user}')

    # And then, Issue access_token and refresh_token.
    access_token = issue_token(user_info=created_user.to_dict(), delta=timedelta(hours=1))
    refresh_token = issue_token(user_info=created_user.to_dict(), delta=timedelta(days=14))

    # And then, Update user info with `refresh_token`.
    await create_user_tokens(db=db, user_id=created_user.user_id, refresh_token=refresh_token)

    return SuccessResponse(message='Successfully created user.',
                           user=created_user.to_dict(),
                           access_token=access_token,
                           refresh_token=refresh_token,
                           status_code=status.HTTP_201_CREATED)


@router.get('/all')
async def get_all_users(token_payload: dict = Depends(check_auth_using_token),
                        db: Session = Depends(get_db)):
    """
    Only `admin` authorization can get this endpoint.
    """
    logging.info('GET /user/all')
    if isinstance(token_payload, RefreshTokenExpired) or isinstance(token_payload, AccessTokenExpired):
        logging.debug('One of tokens is expired.')
        return JSONResponse(content={
            'success': False,
            'detail': token_payload.detail
        }, status_code=token_payload.status_code)

    # If not admin, You can't use this endpoint.
    auth = token_payload['authorization']
    if auth != 'admin':
        logging.debug('this user has admin authorization.')
        return FailureResponse(message='Not enough authorization to do this.',
                               status_code=status.HTTP_401_UNAUTHORIZED)

    users = await read_users(db)
    logging.debug(f'users: {users}')

    return SuccessResponse(users=[user.to_dict() for user in users])


@router.get('/{user_id}')
async def user_read(user_id: int,
                    token_payload: dict = Depends(check_auth_using_token),
                    db: Session = Depends(get_db)):
    """
    When you want to get user info from database.
    You must input `user_id` or `email`. One of them!
    The tokens are just needed to be valid.
    Don't check who's token.
    """
    logging.info('GET /user/')
    if isinstance(token_payload, RefreshTokenExpired) or isinstance(token_payload, AccessTokenExpired):
        logging.debug('One of tokens is expired.')
        return FailureResponse(message=token_payload.detail, status_code=token_payload.status_code)

    result = await read_user(user_id=user_id, db=db)
    logging.debug(f'user: {result}')

    if result is not None:
        return SuccessResponse(user=result.to_dict())
    else:
        return FailureResponse(message='No such user.', status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{user_id}')
@router.patch('/{user_id}')
async def update_user_info(user_info: UserInformation,
                           token_payload: dict = Depends(check_auth_using_token),
                           user_id: int | None = Path(default=None, description='One of way to select user.'),
                           db: Session = Depends(get_db)):
    """
    When you want to update user's information.
    Put user information you want to update on **request body**.
    Use `user_id`.
    """
    logging.info('PATCH /user/')
    if isinstance(token_payload, RefreshTokenExpired) or isinstance(token_payload, AccessTokenExpired):
        logging.debug('One of tokens is expired.')
        return FailureResponse(message=token_payload.detail, status_code=token_payload.status_code)

    # To update user's information, Be admin or client itself.
    auth = token_payload['authorization']
    client_user_id = token_payload['user_id']
    if auth == 'admin' or user_id == client_user_id:
        # Check authorization first.
        if not await read_authorization(user_info.authorization, db):
            logging.debug('No such authorization.')
            return FailureResponse(message='No such authorization.', status_code=status.HTTP_404_NOT_FOUND)

        # If authorization exists, Fix user information.
        rows = await update_user(db=db, user_id=user_id,
                                 email=user_info.email,
                                 name=user_info.name,
                                 thumbnail_url=user_info.thumbnail_url,
                                 authorization_name=user_info.authorization)

        if not rows:
            logging.debug('Not updated.')
            return FailureResponse(message='Not updated.', status_code=status.HTTP_403_FORBIDDEN)
        else:
            user = await read_user(db=db, user_id=user_id)
            logging.debug(f'user: {user}')
            return SuccessResponse(message='Successfully updated.', user=user.to_dict())
    else:
        logging.debug('client hasn\'t admin authorization or user_id is not correct.')
        return FailureResponse(message='No authorization to do this.', status_code=status.HTTP_401_UNAUTHORIZED)



@router.delete('/{user_id}')
async def remove_user(user_id: int,
                      token_payload: dict = Depends(check_auth_using_token),
                      db: Session = Depends(get_db)):
    logging.info('DELETE /user/')
    if isinstance(token_payload, RefreshTokenExpired) or isinstance(token_payload, AccessTokenExpired):
        logging.debug('One of tokens is expired.')
        return FailureResponse(message=token_payload.detail, status_code=token_payload.status_code)

    auth = token_payload['authorization']
    client_user_id = int(token_payload['user_id'])
    logging.debug(f'auth: {auth}')
    logging.debug(f'client_user_id: {client_user_id}')
    logging.debug(f'user_id: {user_id}')

    is_admin = auth == 'admin'
    is_same_user = user_id == client_user_id
    if is_admin or is_same_user:
        await delete_user_tokens(user_id=user_id, db=db)
        rows = await delete_user(user_id=user_id, db=db)
        logging.debug(f'deleted count: {rows}')

        if not rows:
            logging.debug('Not deleted.')
            return FailureResponse(message='Not deleted.', status_code=status.HTTP_404_NOT_FOUND)

        return SuccessResponse(message='Successfully deleted.', count=rows)
    else:
        logging.debug('No authorization to do this.')
        return FailureResponse(message='No authorization to do this.', status_code=status.HTTP_401_UNAUTHORIZED)
