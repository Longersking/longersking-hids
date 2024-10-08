# models/base.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config.base import mysql_username,mysql_password,mysql_host,mysql_port,mysql_db


# 数据库连接字符串
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{mysql_username}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}"

# 创建数据库引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL,pool_pre_ping=True)

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 基础模型
Base = declarative_base()

Base.metadata.create_all(bind=engine)


