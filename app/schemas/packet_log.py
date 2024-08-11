from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PacketLogResponse(BaseModel):
    id: int
    host_ip: Optional[str]
    src_ip: Optional[str]
    src_port: Optional[str]
    dst_ip: Optional[str]
    dst_posrt: Optional[str]
    potocol: Optional[str]
    pack_size: Optional[float]
    content: Optional[str]
    is_dangerous: Optional[int]
    match: Optional[str]
    create_time: datetime

    class Config:
        orm_mode = True