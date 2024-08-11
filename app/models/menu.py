from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, DECIMAL
from .base import Base


class Menu(Base):
    __tablename__ = 'menu_list'

    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)
    icon = Column(String(100))
    url = Column(String(255),nullable=False)
    create_time = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

