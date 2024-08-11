from pydantic import BaseModel
# pydantic模型
class DisIpItem(BaseModel):
    id: int
    host_ip:str
    ip: str
    create_time: str
    operator: int


class addIP(BaseModel):
    ip: str
    operator: int