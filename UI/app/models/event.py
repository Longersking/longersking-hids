# models/event.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .base import Base

class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(50), nullable=False)
    description = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
