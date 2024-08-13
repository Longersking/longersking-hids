from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from .base import Base
from datetime import datetime

class FileLog(Base):
    __tablename__ = "file_log"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String(1000), nullable=True, comment='主机IP')
    file_path = Column(String(1000), nullable=True, comment='文件路径')
    action = Column(String(1000), nullable=True, comment='变更类型')
    is_dir = Column(Integer, nullable=True, comment='是否为目录')
    size = Column(Float, nullable=True, comment='文件尺寸')
    owner = Column(String(255), nullable=True, comment='所属者')
    desc = Column(String(1000), nullable=True, comment='描述')
    is_alarms = Column(Integer, nullable=True, comment='是否为警告')
    content = Column(Text, nullable=True, comment='文件内容')
    file_create_time = Column(DateTime, nullable=True, comment='文件创建时间')
    file_modify_time = Column(DateTime, nullable=True, comment='文件操作时间')
    update_time = Column(DateTime, nullable=True, comment='上次修改时间')
    log_time = Column(DateTime, default=datetime.utcnow, comment='记录时间')
