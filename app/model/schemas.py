from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    name: str
    thumbnail_url: str | None


class UserInformation(UserBase):
    authorization: str


class UserCreate(UserInformation):
    github_id: int


class User(UserBase):
    user_id: int
    uuid: str

    created_at: datetime

    class Config:
        orm_mode = True


"""

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer(), autoincrement=True, unique=True, primary_key=True, nullable=False)
    uuid = Column(String(25), unique=True, nullable=False)

    github_id = Column(String(100), unique=True, nullable=True)

    email = Column(String(100), unique=True, nullable=True)
    name = Column(String(100), unique=False, nullable=True)

    # `func.now()` means `TIMESTAMP.NOW()`.
    created_at = Column(TIMESTAMP(), nullable=False, default=func.now())

    authorization = Column(String(25), ForeignKey('authorizations.name'))

"""


class AuthorizationBase(BaseModel):
    name: str


class Authorization(AuthorizationBase):
    uuid: str
    created_at: datetime

    class Config:
        orm_mode = True


"""

class Authorization(Base):
    __tablename__ = 'authorizations'

    uuid = Column(String(25), unique=True, nullable=False, primary_key=True)
    name = Column(String(25), nullable=False)
    created_at = Column(TIMESTAMP(), nullable=False, default=func.now())

"""


class ChannelBase(BaseModel):
    channel_name: str


class ChannelCreate(ChannelBase):
    ...


class Channel(ChannelCreate):
    uuid: str
    channel_name: str = "Untitled"
    channel_id: int
    created_at: datetime

    class Config:
        orm_mode = True

    class ChannelMember:
        name: str


class ChatBase(BaseModel):
    content: str
    chatter_id: int


class ChatCreate(ChatBase):
    ...


class Chat(ChatCreate):
    uuid: str
    chat_id: int
    created_at: datetime

    class Config:
        orm_mode = True


"""

class Chat(Base, SerializerMixin):
    __tablename__ = 'chats'

    uuid = Column(String(50), unique=True, nullable=False, primary_key=True)
    chat_id = Column(Integer(), autoincrement=True, unique=True, nullable=False)
    content = Column(String(4000), nullable=False)
    chatter_id = Column(Integer(), ForeignKey('users.user_id'), nullable=False)
    created_at = Column(TIMESTAMP(), default=func.now(), nullable=False)

"""


class UserTokenBase(BaseModel):
    user_id: int


class UserTokenCreate(UserTokenBase):
    refresh_token: str | None


class UserToken(UserTokenCreate):
    uuid: str
    github_id: int

    class Config:
        orm_mode = True


"""

class UserToken(Base, SerializerMixin):
    __tablename__ = 'user_tokens'

    uuid = Column(String(50), unique=True, nullable=False, primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.user_id'))
    github_id = Column(Integer(), ForeignKey('users.github_id'))
    refresh_token = Column(String(1000), unique=True, nullable=True)

"""


class File(BaseModel):
    uuid: str
    file_id: int
    file_name: str
    file_binary: bytes
    created_at: datetime

    class Config:
        orm_mode = True


"""

class File(Base, SerializerMixin):
    __tablename__ = 'files'

    uuid = Column(String(50), unique=True, nullable=False, primary_key=True)
    file_id = Column(Integer(), autoincrement=True, unique=True, nullable=False)
    file_name = Column(String(100), nullable=False, default=str(func.now()))
    file_binary = Column(LargeBinary(), nullable=False)
    created_at = Column(TIMESTAMP(), default=func.now(), nullable=False)

"""


class ChatHistory(BaseModel):
    uuid: str
    history_id: int
    channel_id: int
    chat_id: int
    file_id: int

    class Config:
        orm_mode = True


"""

class ChatHistory(Base, SerializerMixin):
    __tablename__ = 'chat_history'

    uuid = Column(String(50), unique=True, nullable=False, primary_key=True)
    history_id = Column(Integer(), autoincrement=True)
    channel_id = Column(Integer(), ForeignKey('channels.channel_id'), nullable=False)
    chat_id = Column(Integer(), ForeignKey('chats.chat_id'), nullable=True)
    file_id = Column(Integer(), ForeignKey('files.file_id'), nullable=True)

"""
