# models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime,func
# from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime
from .base import Base, engine


class IpDisabled(Base):
    __tablename__ = "ip_disabled"
    id = Column(Integer, primary_key=True, index=True)
    host_ip = Column(String(100), unique=True)
    ip = Column(String(100), unique=True)
    create_time = Column(DateTime,default=func.now())
    operator = Column(Integer)


Base.metadata.create_all(bind=engine)
