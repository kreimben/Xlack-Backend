import logging
import uuid

from sqlalchemy.orm import Session

from app.model import models


async def create_history(db: Session, channel_id: int,
                         chat_id: int | None = None,
                         file_id: int | None = None) -> models.ChatHistory:
    history = models.ChatHistory(uuid=str(uuid.uuid4()),
                                 channel_id=channel_id,
                                 chat_id=chat_id,
                                 file_id=file_id)
    logging.debug(f'history: {history.to_dict()}')
    db.add(history)
    db.commit()
    db.refresh(history)
    return history


async def read_history(db: Session, channel_id: int) -> models.ChatHistory:
    history = db.query(models.ChatHistory).filter(models.ChatHistory.channel_id == channel_id).first()
    logging.debug(f'history: {history}')
    return history


async def delete_history(db: Session, channel_id: int) -> models.ChatHistory:
    rows = db.query(models.ChatHistory).filter(models.ChatHistory.channel_id == channel_id).delete()
    db.commit()
    return rows
