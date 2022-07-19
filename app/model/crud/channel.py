import uuid

from sqlalchemy.orm import Session

from app.model import models


async def create_channel(db: Session, channel_name: str) -> models.Channel:
    channel = models.Channel(uuid=str(uuid.uuid4()), channel_name=channel_name)
    db.add(channel)
    db.commit()
    db.refresh(channel)
    return channel


async def read_channel(db: Session, channel_id: int) -> models.Channel:
    return db.query(models.Channel) \
        .filter(models.Channel.channel_id == channel_id) \
        .first()


async def read_channels(db: Session) -> [models.Channel]:
    return db.query(models.Channel).all()


async def update_channel(db: Session, channel_id: int, new_channel_name: str) -> int:
    channel_update = db.query(models.Channel) \
        .filter(models.Channel.channel_id == channel_id) \
        .update({'channel_name': new_channel_name})
    db.commit()
    return channel_update


async def delete_channel(db: Session, channel_id: int) -> int:
    rows = db.query(models.Channel) \
        .filter(models.Channel.channel_id == channel_id) \
        .delete()
    db.commit()
    return rows
