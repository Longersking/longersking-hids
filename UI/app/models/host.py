from sqlalchemy.dialects.mysql import BIGINT,DECIMAL,DATE,TIME,DATETIME #导入字段
from sqlalchemy import Column #字段
from .base import Base,engine


# """
# id主键
# percent使用率
# total总量
# used使用量
# free剩余量
# create_date 创建日期
# create_time 创建时间
# create_dt 创建日期时间
# """
#内存
class Mem(Base):
    __tablename__ = "mem" #指定表名
    id = Column(BIGINT,primary_key=True)
    percent = Column(DECIMAL(6,2)) #保留6位有效数字，保留两位小数
    total = Column(DECIMAL(8,2))
    used = Column(DECIMAL(8,2))
    free = Column(DECIMAL(8,2))
    create_date = Column(DATE)
    create_time = Column(TIME)
    create_dt = Column(DATETIME)


# 交换分区
class SwapPartition(Base):
    __tablename__ = "swap_partition" #指定表名
    id = Column(BIGINT, primary_key=True)
    percent = Column(DECIMAL(6, 2))  # 保留6位有效数字，保留两位小数
    total = Column(DECIMAL(8, 2))
    used = Column(DECIMAL(8, 2))
    free = Column(DECIMAL(8, 2))
    create_date = Column(DATE)
    create_time = Column(TIME)
    create_dt = Column(DATETIME)

#cpu模型
class Host(Base):
    __tablename__ = "cpu"  # 指定表名
    id = Column(BIGINT, primary_key=True)
    percent = Column(DECIMAL(6, 2))  # 保留6位有效数字，保留两位小数
    create_date = Column(DATE)
    create_time = Column(TIME)
    create_dt = Column(DATETIME)


Base.metadata.create_all(bind=engine)
