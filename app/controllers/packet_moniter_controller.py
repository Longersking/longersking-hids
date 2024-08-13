from datetime import datetime
import json
from typing import List, Optional
from app.schemas.packet_log import PacketLogResponse
from app.controllers.alert_controller import write_alert
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.database import SessionLocal
from app.models.packet_log import PacketLog  # 确保 PacketLog 模型已经定义
from fastapi import APIRouter, Depends

router = APIRouter()

def process_packet_data(data_json: dict):
    """
    处理并将 WebSocket 中接收到的 packet_monitor 数据写入数据库
    :param data_json: 从 WebSocket 接收到的数据字典
    :param db: 数据库 session
    """

    db = SessionLocal()
    packet_data = json.loads(data_json['data'])

    # 检查是否为警告包
    if packet_data['is_dangerous'] == 1:
        # 遍历match并且写入告警记录
        for item in packet_data['matches']:
            write_alert(
                type = "packet_alert",
                level = item['severity'],
                ip = data_json['ip'],
                desc = item['description'],
                application = "Web",
                snapshot = json.dumps(packet_data),
                source_ip = packet_data['src_ip'],
                port = packet_data['src_port'],
                target_ip = packet_data['dst_ip'],
                target_port = packet_data['dst_port'],
                create_time=datetime.now(),
            )

    # 映射数据到数据库模型
    packet_log = PacketLog(
        host_ip= data_json['ip'],
        src_ip=packet_data.get('src_ip'),
        src_port=packet_data.get('src_port'),
        dst_ip=packet_data.get('dst_ip'),
        dst_posrt=packet_data.get('dst_port'),  # 注意这里可能有错别字，确认字段名称正确
        potocol=packet_data.get('protocol'),
        pack_size=packet_data.get('size'),
        content=json.dumps(packet_data.get('content')),  # 将内容转为 JSON 字符串保存
        is_dangerous=0 if packet_data['is_dangerous'] is None else int(packet_data['is_dangerous']),  # 初始值为 0 表示没有风险，可以根据业务逻辑判断是否有风险
        match=json.dumps(packet_data['matches']) if packet_data['matches'] is not None else "",  # 初始为空，可以在后续逻辑中根据内容进行匹配填充
        create_time=datetime.now()
    )

    # 将数据写入数据库
    db.add(packet_log)
    db.commit()

@router.get("/get")
def get_packet_logs(
        page: int = 1,
        page_size: int = 20,
        src_ip: Optional[str] = None,
        dst_ip: Optional[str] = None,
        protocol: Optional[str] = None,
        is_dangerous: Optional[str] = None,
):
    db = SessionLocal()
    query = db.query(PacketLog)

    if src_ip:
        query = query.filter(PacketLog.src_ip == src_ip)
    if dst_ip:
        query = query.filter(PacketLog.dst_ip == dst_ip)
    if protocol:
        query = query.filter(PacketLog.potocol == protocol)

    if is_dangerous is not None:
        query = query.filter(PacketLog.is_dangerous == int(is_dangerous))

    total = query.count()
    logs = query.order_by(desc(PacketLog.id)).offset((page - 1) * page_size).limit(page_size).all()

    return {"logs": logs, "total": total}