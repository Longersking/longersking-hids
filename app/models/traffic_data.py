from sqlalchemy import Column, String, Float, DateTime, JSON, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class TrafficData(Base):
    __tablename__ = 'traffic_data'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ip = Column(String, index=True)
    total_sent = Column(Float)
    total_received = Column(Float)
    protocol_sizes = Column(JSON)
    timestamp = Column(DateTime, default=datetime.now())
