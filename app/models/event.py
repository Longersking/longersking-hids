# models/event.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .base import Base, engine


class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(50), nullable=False)
    description = Column(Text)
    timestamp = Column(DateTime, default=datetime.now())

class UserLog(Base):
    __tablename__ = "user_log"
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(Integer, nullable=False)
    ip = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    login_time = Column(String(100))


Base.metadata.create_all(bind=engine)