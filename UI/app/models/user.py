# models/user.py
from sqlalchemy import Column, Integer, String, Boolean
# from sqlalchemy.orm import relationship
from .base import Base,engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    # email = Column(String(100))
    disabled = Column(Boolean, default=False)
    hashed_password = Column(String(100), nullable=False)
    role = Column(String(50))
    avatar = Column(String(1000))
    create_time = Column(String(1000))

Base.metadata.create_all(bind=engine)
