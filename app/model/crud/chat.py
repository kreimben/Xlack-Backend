import uuid

from sqlalchemy.orm import Session

import app.model.models
from app.model import models


async def create_chat(db: Session,
                      content: str,
                      chatter_id: int,
                      channel_id=app.model.models.Channel.channel_id) -> models.Chat:
    chat = models.Chat(uuid=str(uuid.uuid4()),
                       content=content,
                       chatter_id=chatter_id,
                       channel_id=channel_id)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


async def read_chat(db: Session, chat_id: int) -> models.Chat:
    return db.query(models.Chat).filter(models.Chat.chat_id == chat_id).first()


async def read_chats(db: Session) -> [models.Chat]:
    return db.query(models.Chat).all()


async def update_chat(db: Session, chat_id: int, new_chat_content: str) -> int:
    chat_updated = db.query(models.Chat). \
        filter(models.Chat.chat_id == chat_id) \
        .update({'content': new_chat_content})
    db.commit()
    return chat_updated


async def delete_chat(db: Session, chat_id: int) -> int:
    chat_deleted = db \
        .query(models.Chat) \
        .filter(models.Chat.chat_id == chat_id) \
        .delete()
    db.commit()
    return chat_deleted

# async def save_chat_history(db: Session, chat_id: int, chanel_id: int, file_id: int)->models.Chat:
# TODO: how to make history file with class ChatHistory in models.py. I think I should search for using this
