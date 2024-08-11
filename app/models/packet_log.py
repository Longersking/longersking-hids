from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from .base import Base  # 确保这个路径正确

class PacketLog(Base):
    __tablename__ = "packet_log"

    id = Column(Integer, primary_key=True, index=True)
    host_ip = Column(String,nullable=True)
    src_ip = Column(String(255), nullable=True, comment='源IP地址')
    src_port = Column(String(255), nullable=True, comment='源端口')
    dst_ip = Column(String(255), nullable=True, comment='目标IP')
    dst_posrt = Column(String(255), nullable=True, comment='目标端口')
    potocol = Column(String(100), nullable=True, comment='协议')
    pack_size = Column(Float, nullable=True, comment='包大小')
    content = Column(String(), nullable=True, comment='包内容')
    is_dangerous = Column(Integer, nullable=True, comment='是否存在风险', default=0)
    match = Column(String(), nullable=True, comment='报警命中')
    create_time = Column(DateTime, nullable=True, comment='创建时间', default=datetime.now())
