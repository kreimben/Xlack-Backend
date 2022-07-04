from fastapi import Depends
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models
import uuid

"""
This functions are not capable to auth every actions.
"""


async def create_authorization(name: str, db: Session = Depends(get_db)) -> models.Authorization:
    """
    Create authorization into database.

    :param name:
    :param db:
    :return:
    """
    user = models.Authorization(uuid=str(uuid.uuid4()), name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def read_authorization(name: str, db: Session = Depends(get_db)) -> models.Authorization:
    return db.query(models.Authorization).filter(models.Authorization.name == name).first()


async def read_authorizations(db: Session = Depends(get_db)) -> [models.Authorization]:
    return db.query(models.Authorization).all()


async def update_authorization(old_name: str, new_name: str, db: Session = Depends(get_db)) -> models.Authorization:
    auth = db.query(models.Authorization).filter(models.Authorization.name == old_name).update({'name': new_name})
    db.commit()
    db.refresh(auth)
    return auth


async def delete_authorization(name: str, db: Session = Depends(get_db)) -> int:
    rows = db.query(models.Authorization).filter(models.Authorization.name == name).delete()
    db.commit()
    return rows
