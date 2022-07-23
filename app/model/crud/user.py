import uuid

from sqlalchemy.orm import Session

from app.model import models

"""
This functions are not capable to authentication every actions.
"""


async def create_user(db: Session,
                      github_id: int,
                      email: str,
                      name: str,
                      thumbnail_url: str | None = None,
                      authorization_name: str = 'member') -> models.User:
    """
    Create user into database.

    :param thumbnail_url: Thumbnail image url from GitHub user info.
    :param github_id: GitHub id provided by GitHub.
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
                       authorization=authorization_name,
                       thumbnail_url=thumbnail_url)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def read_user(db: Session,
                    user_id: int | None = None,
                    github_id: int | None = None) -> models.User:
    """
    Return user data using one of parameter below.
    """
    if github_id is not None:
        return db.query(models.User).filter(models.User.github_id == github_id).first()
    elif user_id is not None:
        return db.query(models.User).filter(models.User.user_id == user_id).first()


async def read_users(db: Session) -> [models.User]:
    return db.query(models.User).all()


async def update_user(db: Session,
                      user_id: int,
                      email: str,
                      name: str,
                      thumbnail_url: str | None = None,
                      authorization_name: str = 'guest') -> models.User:
    """
    Identify user only with **user_id**!!!
    Check authorization first!!!

    :param authorization_name: Check GET `/authorization/all` first.
    :param thumbnail_url: Thumbnail image url from GitHub user info you want to fix.
    :param user_id: Using when identifying user.
    :param email: Field to update.
    :param name: Field to update.
    :param authorization_name: Field to update. Not required.
    :param db:
    :return:
    """

    user = db \
        .query(models.User) \
        .filter(models.User.user_id == user_id) \
        .update({'email': email,
                 'name': name,
                 'authorization': authorization_name,
                 'thumbnail_url': thumbnail_url})
    db.commit()

    return user


async def delete_user(user_id: int, db: Session) -> int:
    """
    Delete user using `user_id`. This function doesn't check authorization.

    :param user_id: Using when identifying user.
    :param db:
    :return:
    """
    rows = db.query(models.User).filter(models.User.user_id == user_id).delete()
    db.commit()
    return rows
