from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.host import Host
from app.models.user import User
from app.schemas.host import HostCreate, HostResponse
from typing import List
from app.controllers.user_controller import get_current_user
from app.common import dataReturn
import json
router = APIRouter()

@router.get("/get")
# def get_hosts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
def get_hosts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # if current_user.role == 'admin':
    #     hosts = db.query(Host).offset(skip).limit(limit).all()
    # else:
    #     hosts = db.query(Host).filter(Host.user_id == current_user.id).offset(skip).limit(limit).all()
    hosts = db.query(Host).offset(skip).limit(limit).all()
    return dataReturn(1,"获取成功",hosts)

@router.get("/search", response_model=List[HostResponse])
def search_hosts(ip: str = None, last_update: str = None, db: Session = Depends(get_db)):
    query = db.query(Host)
    # if current_user.role != 'admin':
    #     query = query.filter(Host.user_id == current_user.id)
    if ip:
        query = query.filter(Host.host_ip == ip)
    # if user_id and current_user.role == 'admin':
    #     query = query.filter(Host.user_id == user_id)
    if last_update:
        query = query.filter(Host.last_update >= last_update)
    return query.all()

@router.post("/add", response_model=HostResponse)
def create_host(host: HostCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    if current_user['data'].role != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized to create hosts.")
    # 检查主机IP是否已存在
    existing_host = db.query(Host).filter(Host.host_ip == host.host_ip).first()
    if existing_host:
        raise HTTPException(status_code=400, detail="主机IP已存在。")

    # 创建新的主机实例
    db_host = Host(
        host_ip=host.host_ip,
        operating_system=host.operating_system,
        alias=host.alias,
        cpu_cores=host.cpu_cores,
        total_memory_gb=host.total_memory_gb,
        total_disk_space_gb=host.total_disk_space_gb,
        network_bandwidth_mbps=host.network_bandwidth_mbps,
        notes=host.notes
    )
    db.add(db_host)
    db.commit()
    db.refresh(db_host)
    return db_host


@router.get("/data/{ip}")
def get_host_data(ip: str, db: Session = Depends(get_db)):
    # 这里假设从某个地方获取主机的状态数据
    # 你可以使用一个实际的监控工具或系统命令来获取实时数据
    # 这里我们将返回示例数据
    example_data = {
        "cpu": {
            "percent_avg": 0.6,
            "percent_per": [1.0, 0.0, 1.0, 0.0, 1.9, 0.0, 1.0, 0.0],
            "num_physic": 4,
            "num_logic": 8
        },
        "mem": {
            "total": 15.0,
            "used": 5.08,
            "free": 0.45,
            "percent": 36.0
        },
        "swap_memory": {
            "total": 0.0,
            "used": 0.0,
            "free": 0.0,
            "percent": 0.0
        },
        "disk": [{
            "device": "/dev/vda1",
            "mountpoint": "/",
            "fstype": "ext4",
            "opts": "rw,relatime,data=ordered",
            "used": {
                "total": 196.73,
                "used": 76.34,
                "free": 112.18,
                "percent": 40.5
            }
        }],
        "net": [{
            "name": "eth0",
            "bytes_sent": 79552371530,
            "bytes_recv": 75116131625,
            "packets_sent": 54285416,
            "packets_recv": 96740911,
            "family": "AF_INET",
            "address": "172.16.136.122",
            "netmask": "255.255.240.0",
            "broadcast": "172.16.143.255"
        }, {
            "name": "lo",
            "bytes_sent": 406778489591,
            "bytes_recv": 406778489591,
            "packets_sent": 2807030250,
            "packets_recv": 2807030250,
            "family": "AF_INET",
            "address": "127.0.0.1",
            "netmask": "255.0.0.0",
            "broadcast": None
        }],
        "lastest_start_time": "2024-04-02 00:57:29",
        "logined_users": [{
            "name": "root",
            "terminal": "pts/0",
            "host": "localhost",
            "started": "2024-08-05 02:11:45",
            "pid": 28263
        }, {
            "name": "root",
            "terminal": "pts/1",
            "host": "localhost",
            "started": "2024-08-05 02:27:41",
            "pid": 29675
        }]
    }

    # 将示例数据转换为 JSON 字符串并返回
    return dataReturn(1, "获取成功", json.dumps(example_data))