from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class FileLogBase(BaseModel):
    id:Optional[int]
    ip:Optional[str] = None
    file_path: Optional[str]
    action: Optional[str]
    is_dir: Optional[int]
    size: Optional[float]
    owner: Optional[str]
    desc: Optional[str]
    is_alarms: Optional[int]
    content: Optional[str]
    file_create_time: Optional[datetime]
    file_modify_time: Optional[datetime]
    update_time: Optional[datetime]
    log_time: Optional[datetime]

class FileLogCreate(FileLogBase):
    pass

class FileLogResponse(FileLogBase):
    id: int

    class Config:
        orm_mode = True
