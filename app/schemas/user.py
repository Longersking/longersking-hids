from pydantic import BaseModel
from typing import Union
from datetime import datetime

class UserCreate(BaseModel):
    username: Union[str, int]
    # email: str
    password: Union[str, int]
    role: str = "user"
    create_time:str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class UserInfo(BaseModel):
    id: int
    username: str
    disabled: int
    role: str
    avatar: Union[str, None]
    create_time: str