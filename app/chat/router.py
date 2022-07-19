import logging

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from starlette import status

from app.errors.jwt_error import AccessTokenExpired, RefreshTokenExpired
from app.model.crud.chat import create_chat, read_chat, read_chats, update_chat, delete_chat
from app.model.database import get_db
from app.model.schemas import Chat, ChatCreate
from app.utils.jwt import check_auth_using_token
from app.utils.responses import FailureResponse, SuccessResponse

router = APIRouter(prefix='/chat', tags=['chat'])


@router.post('/', response_model=Chat)
async def chat_create(chat: ChatCreate,
                      db: Session = Depends(get_db),
                      token_payload=Depends(check_auth_using_token)):
    logging.info('POST /chat/')

    # Check auth from dependency
    if isinstance(token_payload, AccessTokenExpired) or isinstance(token_payload, RefreshTokenExpired):
        logging.debug('One of tokens is expired.')
        return FailureResponse(message=token_payload.detail, status_code=token_payload.status_code)

    if token_payload['authorization'] == 'guest':
        logging.debug('guest is going to create channel')
        return FailureResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                               message='Guest can\'t read channel')

    db_chat = await create_chat(db=db,
                                content=chat.content,
                                chatter_id=chat.chatter_id)
    logging.debug(f'chat: {chat}')

    return SuccessResponse(message='Successfully Created Chat', chat=db_chat.to_dict())


@router.get('/', response_model=Chat)
async def chat_read(chat_id: int,
                    db: Session = Depends(get_db),
                    token_payload=Depends(check_auth_using_token)):
    logging.info('GET /chat/')

    # Check auth from dependency
    if isinstance(token_payload, AccessTokenExpired) or isinstance(token_payload, RefreshTokenExpired):
        logging.debug('One of tokens is expired.')
        return FailureResponse(message=token_payload.detail, status_code=token_payload.status_code)

    if token_payload['authorization'] == 'guest':
        logging.debug('guest is going to create channel')
        return FailureResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                               message='Guest can\'t read channel')

    chat = await read_chat(db, chat_id=chat_id)

    return SuccessResponse(chat=chat.to_dict())


@router.get('/all', response_model=Chat)
async def show_chat_all(db: Session = Depends(get_db),
                        token_payload=Depends(check_auth_using_token)):
    logging.info('GET /chat/all')

    # Check auth from dependency
    if isinstance(token_payload, AccessTokenExpired) or isinstance(token_payload, RefreshTokenExpired):
        logging.debug('One of tokens is expired.')
        return FailureResponse(message=token_payload.detail, status_code=token_payload.status_code)

    if token_payload['authorization'] == 'guest':
        logging.debug('guest is going to create channel')
        return FailureResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                               message='Guest can\'t read channel')

    all_chat = await read_chats(db)
    logging.debug(f'all chats: {all_chat}')
    return SuccessResponse(chats=[chat.to_dict() for chat in all_chat])


@router.patch('/{chat_id}', response_model=Chat)
async def chat_update(chat_id: int,
                      new_chat_content: str = Body(...),
                      db: Session = Depends(get_db),
                      token_payload=Depends(check_auth_using_token)):
    logging.info('PATCH /channel/{chat_id}')

    # Check auth from dependency
    if isinstance(token_payload, AccessTokenExpired) or isinstance(token_payload, RefreshTokenExpired):
        logging.debug('One of tokens is expired.')
        return FailureResponse(message=token_payload.detail, status_code=token_payload.status_code)

    if token_payload['authorization'] == 'guest':
        logging.debug('guest is going to create channel')
        return FailureResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                               message='Guest can\'t read channel')

    await update_chat(db, chat_id=chat_id, new_chat_content=new_chat_content)
    updated_chat = await read_chat(db=db, chat_id=chat_id)
    logging.debug(f'updated chat: {updated_chat}')

    return SuccessResponse(message='Successfully edited chat.', updated_chat=updated_chat.to_dict())


@router.delete('/{chat_id}', response_model=Chat)
async def chat_delete(chat_id: int,
                      db: Session = Depends(get_db),
                      token_payload=Depends(check_auth_using_token)):
    logging.info('DELETE /channel/')

    # Check auth from dependency
    if isinstance(token_payload, AccessTokenExpired) or isinstance(token_payload, RefreshTokenExpired):
        logging.debug('One of tokens is expired.')
        return FailureResponse(message=token_payload.detail, status_code=token_payload.status_code)

    if token_payload['authorization'] == 'guest':
        logging.debug('guest is going to create channel')
        return FailureResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                               message='Guest can\'t read channel')

    rows = await delete_chat(db, chat_id=chat_id)
    logging.debug(f'deleted chat count: {rows}')

    return SuccessResponse(message='Successfully deleted.', count=rows)
