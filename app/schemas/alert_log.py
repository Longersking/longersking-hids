from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AlertLogBase(BaseModel):
    id : Optional[int]
    type: Optional[str] = None
    level: Optional[str] = None
    ip: str
    desc: Optional[str] = None
    application: Optional[str] = None
    snapshot: Optional[str] = None
    source_ip: Optional[str] = None
    port: Optional[str] = None
    target_ip: Optional[str] = None
    target_port: Optional[str] = None
    packet: Optional[str] = None
    create_time: datetime

    class Config:
        orm_mode = True