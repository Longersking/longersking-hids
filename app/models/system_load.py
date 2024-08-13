from sqlalchemy import Column, String, Float, DateTime, JSON, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class SystemLoadData(Base):
    __tablename__ = 'system_load_data'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ip = Column(String, index=True)
    data = Column(String)
    create_time = Column(DateTime, default=datetime.utcnow)
