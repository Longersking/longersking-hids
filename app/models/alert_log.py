from sqlalchemy import Column, Integer, String, Float, DateTime
from .base import Base
from datetime import datetime

class AlertLog(Base):
    __tablename__ = "alert_log"

    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String(50), nullable=False)
    alert_level = Column(String(20), nullable=False)
    ip = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(String(255), nullable=False)
