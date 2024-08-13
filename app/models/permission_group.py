from sqlalchemy import Column, Integer, String,TIMESTAMP,JSON
from .base import Base


class PermissionGroup(Base):
    __tablename__ = 'permission_group'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    menu_nodes = Column(JSON)
    create_time = Column(TIMESTAMP)
