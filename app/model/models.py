import uuid

from sqlalchemy import Column, String, Integer, TIMESTAMP, func, ForeignKey, LargeBinary
from sqlalchemy_serializer import SerializerMixin

from .database import Base


class User(Base, SerializerMixin):
    __tablename__ = 'users'

    user_id = Column(Integer(), autoincrement=True, unique=True, primary_key=True, nullable=False)
    uuid = Column(String(50), unique=True, nullable=False)

    github_id = Column(Integer(), unique=True, nullable=True)

    email = Column(String(100), unique=True, nullable=True)
    name = Column(String(100), nullable=True)

    # `func.now()` means `TIMESTAMP.NOW()`.
    created_at = Column(TIMESTAMP(), nullable=False, default=func.now())

    authorization = Column(String(25), ForeignKey('authorizations.name'))

    thumbnail_url = Column(String(500), nullable=True)


class UserToken(Base, SerializerMixin):
    __tablename__ = 'user_tokens'

    uuid = Column(String(50), unique=True, nullable=False, primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.user_id'), unique=True, nullable=False)
    github_id = Column(Integer(), ForeignKey('users.github_id'), unique=True, nullable=False)
    refresh_token = Column(String(1000), unique=True, nullable=True)


class Authorization(Base, SerializerMixin):
    __tablename__ = 'authorizations'

    uuid = Column(String(50), nullable=False, primary_key=True, default=uuid.uuid4())
    name = Column(String(25), unique=True, nullable=False)
    created_at = Column(TIMESTAMP(), nullable=False, default=func.now())


class Channel(Base, SerializerMixin):
    __tablename__ = 'channels'

    uuid = Column(String(50), unique=True, nullable=False, primary_key=True)
    channel_id = Column(Integer(), autoincrement=True, unique=True, nullable=False)
    channel_name = Column(String(50), unique=True, nullable=False)
    created_at = Column(TIMESTAMP(), default=func.now())


class Chat(Base, SerializerMixin):
    __tablename__ = 'chats'

    uuid = Column(String(50), unique=True, nullable=False, primary_key=True)
    chat_id = Column(Integer(), autoincrement=True, unique=True, nullable=False)
    content = Column(String(4000), nullable=False)
    chatter_id = Column(Integer(), ForeignKey('users.user_id'), nullable=False)
    created_at = Column(TIMESTAMP(), default=func.now(), nullable=False)
    file_id = Column(Integer(), nullable=True)


class File(Base, SerializerMixin):
    __tablename__ = 'files'

    uuid = Column(String(50), unique=True, nullable=False, primary_key=True)
    file_id = Column(Integer(), autoincrement=True, unique=True, nullable=False)
    file_name = Column(String(100), nullable=False, default=str(func.now()))
    file_binary = Column(LargeBinary(), nullable=False)
    created_at = Column(TIMESTAMP(), default=func.now(), nullable=False)


class ChatHistory(Base, SerializerMixin):
    __tablename__ = 'chat_history'

    uuid = Column(String(50), unique=True, nullable=False, primary_key=True)
    history_id = Column(Integer(), autoincrement=True)
    channel_id = Column(Integer(), ForeignKey('channels.channel_id'), nullable=False)
    chat_id = Column(Integer(), ForeignKey('chats.chat_id'), nullable=True)
    file_id = Column(Integer(), ForeignKey('files.file_id'), nullable=True)
