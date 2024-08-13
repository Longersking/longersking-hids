from sqlalchemy import func

from app.models.base import SessionLocal
from app.models.alert_log import AlertLog
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends
from app.models.database import get_db
from app.schemas.alert_log import AlertLogBase

def dataReturn(code: int, msg: str | int, data=None):
    if data != None:
        return {'code': code, 'msg': msg, 'data': data}
    else:
        return {'code': code, 'msg': msg, 'data': data}

router = APIRouter()

def write_alert(**data):
    db = SessionLocal()
    log = AlertLog(
        **data
    )
    db.add(log)
    db.commit()

# 获取告警记录分布
@router.get("/distribution")
def get_alert_distribution(db: Session = Depends(get_db)):
    distribution = db.query(AlertLog.level, func.count(AlertLog.id).label('count')) \
                     .group_by(AlertLog.level) \
                     .all()

    # 转换结果为字典形式
    result = {level_: count for level_, count in distribution}
    return dataReturn(1, "获取告警分布成功", result)

# 查询和筛选告警记录
@router.get("/get")
def get_alerts(
        type: Optional[str] = None,
        level: Optional[str] = None,
        ip: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        page: int = 1,
        size: int = 10,
        db: Session = Depends(get_db)
):
    query = db.query(AlertLog)
    if type:
        query = query.filter(AlertLog.type == type)
    if level:
        query = query.filter(AlertLog.level == level)
    if ip:
        query = query.filter(AlertLog.ip == ip)
    if start_time:
        query = query.filter(AlertLog.create_time >= start_time)
    if end_time:
        query = query.filter(AlertLog.create_time <= end_time)

    total = query.count()  # 获取总条目数
    alerts = query.order_by(desc(AlertLog.id)).offset((page - 1) * size).limit(size).all()  # 分页查询

    return {"alerts": alerts, "total": total}


# 删除告警记录
@router.delete("/del/{alert_id}")
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(AlertLog).filter(AlertLog.id == alert_id).first()
    if alert:
        db.delete(alert)
        db.commit()
        return dataReturn(1, "删除成功！")
    else:
        return dataReturn(0, "删除失败！")
