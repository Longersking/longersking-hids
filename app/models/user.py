from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    role = Column(String(50))
    avatar = Column(String(1000))
    create_time = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    disabled = Column(Integer)
