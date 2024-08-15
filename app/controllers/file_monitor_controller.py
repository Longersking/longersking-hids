from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.database import get_db
from typing import List, Optional
from .alert_controller import write_alert
from app.models.database import SessionLocal
from app.models.file_log import FileLog
from app.schemas.file_log import FileLogCreate, FileLogResponse
import os, re, json

router = APIRouter()


def deal_file_alarms(data_json):
    db = SessionLocal()
    data = json.loads(data_json['data'])
    message = data.get('message', '')
    file_info = data.get('file_info', {})
    event_type = data.get('event_type', '')
    event_path = data.get('event_path', '')

    level = "light"
    source_ip = ""
    source_port = ""
    type = "file_alarms"
    # 如果是用户的登录失败，提取来源IP地址和端口
    if "Failed login attempt detected" in message:
        type = 'user_login'
        level = "medium"
        # 从消息中提取IP和端口
        match = re.search(r'from (\d+\.\d+\.\d+\.\d+) port (\d+)', message)
        if match:
            source_ip = match.group(1)
            source_port = match.group(2)

    alert = dict(
        type=type,
        level=level,
        ip=data_json.get('ip', ''),
        desc=message,
        application="unknown",
        snapshot=json.dumps(data),
        source_ip=source_ip,
        port=source_port,
        target_ip=data_json.get('ip', ''),
        target_port=22,
        create_time=datetime.now()
    )
    record_file_change(data_json)
    print(alert)
    write_alert(**alert)


def record_file_change(data_json):
    db = SessionLocal()
    data = json.loads(data_json['data'])
    file_info = data.get('file_info', {})
    is_alarms = 0
    if data['type'] == "alarms":
        is_alarms = 1
    file_log = FileLog(
        ip=data_json.get('ip', ''),
        file_path=file_info.get('path', ''),
        action=data.get('event_type', ''),
        is_dir=int(os.path.isdir(file_info.get('path', ''))),
        size=file_info.get('size', 0),
        owner=file_info.get('owner', ''),
        desc=data.get('message', ''),
        is_alarms=is_alarms,
        content=file_info.get('content', ''),
        file_create_time=datetime.strptime(file_info.get('creation_time', ''), '%Y-%m-%d %H:%M:%S') if file_info.get(
            'creation_time') else None,
        file_modify_time=datetime.strptime(file_info.get('modification_time', ''),
                                           '%Y-%m-%d %H:%M:%S') if file_info.get('modification_time') else None,
        update_time=datetime.strptime(file_info.get('access_time', ''), '%Y-%m-%d %H:%M:%S') if file_info.get(
            'access_time') else None,
        log_time=datetime.now()
    )

    db.add(file_log)
    db.commit()
    db.refresh(file_log)


@router.get("/get", response_model=List[FileLogResponse])
def get_file_logs(
        response: Response,
        page: int = 1,
        file_path: Optional[str] = None,
        action: Optional[str] = None,
        page_size: int = 20,
        owner: Optional[str] = None,
        db: Session = Depends(get_db)
):
    query = db.query(FileLog)

    if file_path:
        query = query.filter(FileLog.file_path.contains(file_path))
    if action:
        query = query.filter(FileLog.action == action)
    if owner:
        query = query.filter(FileLog.owner.contains(owner))

    total = query.count()
    file_logs = query.order_by(desc(FileLog.id)).offset((page - 1) * page_size).limit(page_size).all()

    response.headers["X-Total-Count"] = str(total)
    return file_logs


@router.post("/file_logs", response_model=FileLogResponse)
def create_file_log(file_log: FileLogCreate, db: Session = Depends(get_db)):
    db_file_log = FileLog(**file_log.dict(), log_time=datetime.now())
    db.add(db_file_log)
    db.commit()
    db.refresh(db_file_log)
    return db_file_log
