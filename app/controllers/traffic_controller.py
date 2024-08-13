from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from ..models.database import get_db
from datetime import datetime
from app.models.traffic_data import TrafficData
from app.models.base import SessionLocal
import json


def insert_traffic_data(data_json):
    db = SessionLocal()
    ip = data_json.get("ip", "")
    traffic_data = json.loads(data_json['data'])
    total_sent = traffic_data.get("total_sent", 0)
    total_received = traffic_data.get("total_received", 0)
    protocol_sizes = traffic_data.get("protocol_sizes", {})
    timestamp = datetime.strptime(data_json.get("time", ""), "%Y-%m-%d %H:%M:%S")
    new_traffic_data = TrafficData(
        ip=ip,
        total_sent=total_sent,
        total_received=total_received,
        protocol_sizes=protocol_sizes,
        timestamp=timestamp
    )
    db.add(new_traffic_data)
    db.commit()
