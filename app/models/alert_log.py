from sqlalchemy import Column, Integer, String, Float, DateTime
from .base import Base
from datetime import datetime

class AlertLog(Base):
    __tablename__ = "alert_log"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(255), nullable=True)
    level = Column(String(255), nullable=True)
    ip = Column(String(255), nullable=False)
    desc = Column(String(1000), nullable=True)
    application = Column(String(1000), nullable=True)
    snapshot = Column(String, nullable=True)
    source_ip = Column(String(255), nullable=True)
    port =  Column(Integer, nullable=True)
    target_ip = Column(String(255), nullable=True)
    target_port = Column(Integer, nullable=True)
    packet = Column(String, nullable=True)
    create_time = Column(DateTime,default=datetime.now())