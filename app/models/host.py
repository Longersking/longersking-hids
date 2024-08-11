from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, DECIMAL
from sqlalchemy.orm import relationship
from .base import Base


class Host(Base):
    __tablename__ = 'host_list'

    host_id = Column(Integer, primary_key=True, autoincrement=True)
    host_ip = Column(String(45), nullable=False)
    operating_system = Column(String(100), nullable=False)
    alias = Column(String(100))
    create_time = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    status = Column(String(20), default='offline')
    cpu_cores = Column(Integer)
    total_memory_gb = Column(DECIMAL(10, 2))
    total_disk_space_gb = Column(DECIMAL(10, 2))
    network_bandwidth_mbps = Column(DECIMAL(10, 2))
    last_update = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')
    notes = Column(String(255))


