from datetime import datetime
from app.models.system_load import SystemLoadData
from app.models.base import SessionLocal
import json


def insert_system_load(data_json):
    db = SessionLocal()
    ip = data_json.get("ip", "")
    data = data_json.get("data", "")
    timestamp = datetime.strptime(data_json.get("time", ""), "%Y-%m-%d %H:%M:%S")
    new_sys_load_data = SystemLoadData(
        ip=ip,
        data=data,
        create_time=timestamp
    )
    db.add(new_sys_load_data)
    db.commit()
