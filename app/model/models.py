from sqlalchemy import Column, String, Integer, TIMESTAMP, func, ForeignKey
import uuid
from .database import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer(), autoincrement=True, unique=True, primary_key=True, nullable=False)
    uuid = Column(String(50), unique=True, nullable=False)

    github_id = Column(String(100), unique=True, nullable=True)

    email = Column(String(100), unique=True, nullable=True)
    name = Column(String(100), nullable=True)

    # `func.now()` means `TIMESTAMP.NOW()`.
    created_at = Column(TIMESTAMP(), nullable=False, default=func.now())

    authorization = Column(String(25), ForeignKey('authorizations.name'))

    refresh_token = Column(String(100), unique=True, nullable=True)


class Authorization(Base):
    __tablename__ = 'authorizations'

    uuid = Column(String(50), nullable=False, primary_key=True, default=uuid.uuid4())
    name = Column(String(25), unique=True, nullable=False)
    created_at = Column(TIMESTAMP(), nullable=False, default=func.now())
