# models/database.py
from .base import SessionLocal

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db  # 使用生成器确保会话在使用后关闭
    finally:
        db.close()

