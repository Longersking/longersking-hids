# models/report.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base
from .event import Event

class Report(Base):
    __tablename__ = "reports"

    report_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    events = relationship("Event", back_populates="report")  # 与事件模型的关系
