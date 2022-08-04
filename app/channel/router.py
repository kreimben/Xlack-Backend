import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.errors.jwt_error import AccessTokenExpired, RefreshTokenExpired
from app.model.crud.channel import create_channel, read_channel, read_channels, delete_channel, update_channel
from app.model.database import get_db
from app.model.schemas import Channel, ChannelCreate
from app.utils.jwt import check_auth_using_token
from app.utils.responses import FailureResponse, SuccessResponse

router = APIRouter(prefix='/channel', tags=['channel'])


@router.post('/')
async def channel_create(channel: ChannelCreate,
                         db: Session = Depends(get_db),
                         token_payload=Depends(check_auth_using_token)):
    logging.info('POST /channel/')

    # Check auth from dependency
    if isinstance(token_payload, AccessTokenExpired) or isinstance(token_payload, RefreshTokenExpired):
        logging.debug('One of tokens is expired.')
        return FailureResponse(message=token_payload.detail, status_code=token_payload.status_code)

    # Guest is not going to create channel. Unauthorized.
    if token_payload['authorization'] == 'guest':
        logging.debug('guest is going to create channel')
        return FailureResponse(message='You can\'t create channel as guest',
                               status_code=status.HTTP_401_UNAUTHORIZED)

    created = await create_channel(db=db, channel_name=channel.channel_name)
    logging.debug(f'channel created: {created}')

    return SuccessResponse(channel=created.to_dict(),
                           message='Successfully created channel',
                           status_code=status.HTTP_201_CREATED)


@router.get('/{channel_id}', response_model=Channel)
async def channel_read_by_name(channel_id: int,
                               db: Session = Depends(get_db),
                               token_payload=Depends(check_auth_using_token)):
    logging.info('GET /channel/')

    # Check auth from dependency
    if isinstance(token_payload, AccessTokenExpired) or isinstance(token_payload, RefreshTokenExpired):
        logging.debug('One of tokens is expired.')
        return FailureResponse(message=token_payload.detail, status_code=token_payload.status_code)

    if token_payload['authorization'] == 'guest':
        logging.debug('guest is going to create channel')
        return FailureResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                               message='Guest can\'t read channel')

    channel = await read_channel(db, channel_id=channel_id)
    logging.debug(f'channels: {channel}')

    return SuccessResponse(channel=channel.to_dict())


@router.get('/all', response_model=Channel)
async def channel_all(db: Session = Depends(get_db),
                      token_payload=Depends(check_auth_using_token)):
    logging.info('GET /channel/all')

    # Check auth from dependency
    if isinstance(token_payload, AccessTokenExpired) or isinstance(token_payload, RefreshTokenExpired):
        logging.debug('One of tokens is expired.')
        return FailureResponse(message=token_payload.detail, status_code=token_payload.status_code)

    if token_payload['authorization'] == 'guest':
        logging.debug('guest is going to create channel')
        return FailureResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                               message='Guest can\'t read channel')

    all_channel = await read_channels(db)
    logging.debug(f'all channels: {all_channel}')
    return SuccessResponse(channels=[channel.to_dict() for channel in all_channel])


@router.patch('/{channel_id}', response_model=Channel)
async def channel_update(channel_id: int,
                         new_channel_name: str,
                         db: Session = Depends(get_db),
                         token_payload=Depends(check_auth_using_token)):
    logging.info('PATCH /channel/')

    # Check auth from dependency
    if isinstance(token_payload, AccessTokenExpired) or isinstance(token_payload, RefreshTokenExpired):
        logging.debug('One of tokens is expired.')
        return FailureResponse(message=token_payload.detail, status_code=token_payload.status_code)

    if token_payload['authorization'] == 'guest':
        logging.debug('guest is going to create channel')
        return FailureResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                               message='Guest can\'t read channel')

    await update_channel(db,
                         channel_id=channel_id,
                         new_channel_name=new_channel_name)

    channel_updated = await read_channel(db=db,
                                         channel_id=channel_id)
    logging.debug(f'updated channel name: {channel_updated}')

    return SuccessResponse(message='Successfully updated channel name.',
                           updated_channel=channel_updated.to_dict())


@router.delete('/{channel_id}', response_model=Channel)
async def channel_delete(channel_id: int,
                         db: Session = Depends(get_db),
                         token_payload=Depends(check_auth_using_token)):
    logging.info('DELETE /channel')

    # Check auth from dependency
    if isinstance(token_payload, AccessTokenExpired) or isinstance(token_payload, RefreshTokenExpired):
        logging.debug('One of tokens is expired.')
        return FailureResponse(message=token_payload.detail, status_code=token_payload.status_code)

    if token_payload['authorization'] == 'guest':
        logging.debug('guest is going to create channel')
        return FailureResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                               message='Guest can\'t read channel')

    rows = await delete_channel(db=db, channel_id=channel_id)
    logging.debug(f'deleted channel count: {rows}')

    if rows != 0:
        return SuccessResponse(message='Successfully Deleted Channel.')
    else:
        return FailureResponse(message='Failed to delete channel', status_code=status.HTTP_404_NOT_FOUND)
