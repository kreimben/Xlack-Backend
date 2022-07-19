import uuid

from sqlalchemy.orm import Session

from app.model import models


async def create_user_tokens(db: Session, user_id: int, refresh_token: str) -> models.UserToken:
    user_token = models.UserToken(uuid=str(uuid.uuid4()),
                                  user_id=user_id,
                                  refresh_token=refresh_token)
    db.add(user_token)
    db.commit()
    db.refresh(user_token)
    return user_token


async def read_user_tokens(db: Session, user_id: int) -> models.UserToken:
    return db.query(models.UserToken).filter(models.UserToken.user_id == user_id).first()


async def update_user_tokens(db: Session, user_id: int, new_refresh_token: str | None) -> int:
    rows = db.query(models.UserToken) \
        .filter(models.UserToken.user_id == user_id) \
        .update({'refresh_token': new_refresh_token})
    db.commit()
    return rows


async def delete_user_tokens(db: Session, user_id: int) -> int:
    rows = db.query(models.UserToken).filter(models.UserToken.user_id == user_id).delete()
    db.commit()
    return rows
