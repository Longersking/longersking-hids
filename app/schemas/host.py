from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HostCreate(BaseModel):
    host_ip: str
    operating_system: str
    alias: str = None
    cpu_cores: int = None
    total_memory_gb: float = None
    total_disk_space_gb: float = None
    network_bandwidth_mbps: float = None
    notes: str = None

class HostResponse(BaseModel):
    host_id: int
    host_ip: str
    operating_system: str
    alias: str = None
    create_time: datetime
    status: str
    cpu_cores: int = None
    total_memory_gb: float = None
    total_disk_space_gb: float = None
    network_bandwidth_mbps: float = None
    last_update: datetime
    notes: str = None