import logging
from typing import Union, List

from fastapi import APIRouter, Body, Cookie, Depends, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from starlette import status

from app.errors.jwt_error import AccessTokenExpired, RefreshTokenExpired
from app.model.crud.chat import create_chat, read_chat, read_chats, update_chat, delete_chat
from app.model.crud.chat_history import create_history
from app.model.database import get_db
from app.model.models import ChatHistory
from app.model.schemas import Channel
from app.model.schemas import Chat, ChatCreate
from app.utils.jwt import check_auth_using_token
from app.utils.responses import FailureResponse, SuccessResponse

router = APIRouter(prefix='/chat', tags=['chat'])


@router.post('/', response_model=Chat)
@router.websocket('/')
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
    # websocket chat start
    db_chat = await create_chat(db=db,
                                content=chat.content,
                                chatter_id=chat.chatter_id,
                                channel_id=Channel.channel_id)
    logging.debug(f'chat: {chat}')

    return SuccessResponse(message='Successfully Created Chat', chat=db_chat.to_dict())


@router.get('/', response_model=Chat)
async def chat_read(chat_id: int,
                    db: Session = Depends(get_db),
                    token_payload=Depends(check_auth_using_token)
                    ):
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


class ConnectionCheck:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_chat(self, chat: str, websocket: WebSocket):
        await websocket.send_text(chat)

    async def broadcast(self, chat: str):
        for connection in self.active_connections:
            await connection.send_text(chat)


check = ConnectionCheck()


@router.websocket('/')
async def websocket_chat(websocket: WebSocket,
                         chatter_id=Chat.chatter_id,
                         query: Union[int, None] = None,
                         token_payload=Depends(check_auth_using_token)):
    # Check auth from dependency
    if isinstance(token_payload, AccessTokenExpired) or isinstance(token_payload, RefreshTokenExpired):
        logging.debug('One of tokens is expired.')
        return FailureResponse(message=token_payload.detail, status_code=token_payload.status_code)

    if token_payload['authorization'] == 'guest':
        logging.debug('guest is going to create channel')
        return FailureResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                               message='Guest can\'t read channel')
    await websocket.accept()
    try:
        while True:
            chat_db = await websocket.receive_text()
            await check.send_personal_chat(f"You:{chat_db}", websocket)
            await check.broadcast(f"from client {chatter_id} chat: {chat_db}")
            if query is not None:
                await websocket.send_text(f"Query parameter query: {query}")

    except WebSocketDisconnect:
        check.disconnect(websocket)
        await check.broadcast(f"chatter {chatter_id} left this chat")


async def get_cookie_or_token(
        websocket: WebSocket,
        session: Union[str, None] = Cookie(default=None),
        token: Union[str, None] = Query(default=None),
):
    if session is None and token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


# endpoint to show chat's cookie or token
@router.websocket('/features/real_chat/items')
async def show_cookie_or_token(websocket: WebSocket, tokens: str = Depends(check_auth_using_token)):
    await websocket.accept()
    while True:
        await websocket.send_text(f"Session cookie : {tokens}")


# TODO: Complete this code with new logic
# FIXME: save chat history not in text file, in db
@router.post('/history')
@router.websocket('/history')
async def save_chat_content(file_id=ChatHistory.file_id,
                            db: Session = Depends(get_db),
                            token_payload=Depends(check_auth_using_token)):
    logging.info('POST /chat/history')
    # Check auth from dependency
    if isinstance(token_payload, AccessTokenExpired) or isinstance(token_payload, RefreshTokenExpired):
        logging.debug('One of tokens is expired.')
        return FailureResponse(message=token_payload.detail, status_code=token_payload.status_code)

    if token_payload['authorization'] == 'guest':
        logging.debug('guest is going to create channel')
        return FailureResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                               message='Guest can\'t read channel')
    chat_history = await create_history(db,
                                        channel_id=Channel.channel_id,
                                        chat_id=Chat.chat_id,
                                        file_id=file_id)
    logging.debug(f'chat: {chat_history}')
    return SuccessResponse(message='Successfully Saved Chat history', chat=chat_history.to_dict())

# TODO: pagination algorithm
