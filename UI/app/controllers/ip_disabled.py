from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List
from ..models.database import get_db
from sqlalchemy.orm import Session
from ..models.ip_disabled import IpDisabled
from pydantic import BaseModel
from .. import common
from datetime import datetime

# 配置路由
ip_route = APIRouter()


# pydantic模型
class DisIpItem(BaseModel):
    id: int
    ip: str
    create_time: str
    operator: int


class addIP(BaseModel):
    ip: str
    operator: int


# 获取被禁用的ip信息
@ip_route.get("/disabled")
async def get(page:int = 1,db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
        获取被封禁的IP
    """
    # 使用 ORM 的 session.query() 并获取所有被封禁的 IP
    ips_query = db.query(IpDisabled).order_by("create_time").limit(10).offset(10*(page-1)).all()
    count = db.query(IpDisabled).count()

    # 将查询结果转换为 Pydantic 模型列表
    ips_list = [DisIpItem(id=ip.id, ip=ip.ip, create_time=str(ip.create_time), operator=ip.operator) for ip in
                ips_query]
    return common.dataReturn(1, msg="disabled_ip", data={"data":ips_list,"total":count})


@ip_route.post("/addDisabled")
async def add(data: addIP, db: Session = Depends(get_db)):
    ip = IpDisabled(ip=data.ip, operator=data.operator, create_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    db.add(ip)
    try:
        db.commit()
        return common.dataReturn(1, "封禁成功")
    except Exception as e:
        db.rollback()
        return common.dataReturn(-1, "写入数据库失败！",e)

@ip_route.get("/delBlack")
async def add(id : int |str, db: Session = Depends(get_db)):
    item = db.query(IpDisabled).filter(IpDisabled.id == id).first()
    db.delete(item)
    try:
        db.commit()
        return common.dataReturn(1, "解禁成功")
    except Exception as e:
        db.rollback()
        return common.dataReturn(-1, "解除封禁失败！",str(e))
