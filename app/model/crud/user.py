from fastapi import Depends
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models
import uuid

"""
This functions are not capable to authentication every actions.
"""


async def create_user(db: Session,
                      github_id: str,
                      email: str,
                      name: str,
                      authorization_name: str = 'member') -> models.User:
    """
    Create user into database.

    :param github_id: github id provided by github.
    :param email: email address.
    :param name: full name.
    :param authorization_name: name which is in `Authorization` in database.
    :param db:
    :return:
    """
    user = models.User(uuid=str(uuid.uuid4()),
                       github_id=github_id,
                       email=email,
                       name=name,
                       authorization=authorization_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def read_user(db: Session,
                    user_id: str | None = None,
                    github_id: str | None = None,
                    email: str | None = None) -> models.User:
    """
    Return user data using one of parameter below.

    :param user_id: Using when identifying user.
    :param github_id: Using when identifying user.
    :param email: Using when identifying user.
    :param db:
    :return: User model.
    """
    if user_id is not None:
        return db.query(models.User).filter(models.User.user_id == user_id).first()
    elif github_id is not None:
        return db.query(models.User).filter(models.User.github_id == github_id).first()
    elif email is not None:
        return db.query(models.User).filter(models.User.email == email).first()


async def read_users(db: Session) -> [models.User]:
    return db.query(models.User).all()


async def update_user(db: Session,
                      user_id: str,
                      email: str,
                      name: str,
                      refresh_token: str,
                      authrization_name: str = 'member') -> models.User:
    """
    Identify user only with **user_id**!!!
    Check authorization first!!!

    :param user_id: Using when identifying user.
    :param email: Field to update.
    :param name: Field to update.
    :param authrization_name: Field to update. (or `None`)
    :param db:
    :return:
    """

    user = db \
        .query(models.User) \
        .filter(models.User.user_id == user_id) \
        .update({'email': email,
                 'name': name,
                 'authrization': authrization_name,
                 'refresh_token': refresh_token})
    db.commit()
    db.refresh(user)
    return user


async def delete_user(user_id: str, db: Session) -> int:
    """
    Delete user using `user_id`. This function doesn't check authorization.

    :param user_id: Using when identifying user.
    :param db:
    :return:
    """
    rows = db.query(models.User).filter(models.User.user_id == user_id).delete()
    db.commit()
    return rows
