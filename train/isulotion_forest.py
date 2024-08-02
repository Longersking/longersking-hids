import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sklearn.ensemble import IsolationForest
import joblib
import sys
import os
import json

# 添加当前文件所在目录的父目录到 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import traffic_data
from app.config import mysql_username, mysql_password, mysql_host, mysql_port, mysql_db

# 创建数据库连接 URL
DATABASE_URL = f"mysql+pymysql://{mysql_username}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}"

# 创建数据库引擎和会话
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def load_data():
    # 创建数据库会话
    session = SessionLocal()
    try:
        # 查询所有流量数据
        query = session.query(traffic_data.TrafficData).all()

        # 解析数据
        data = []
        for row in query:
            protocol_sizes = row.protocol_sizes
            data.append({
                'ip': row.ip,
                'total_sent': row.total_sent,
                'total_received': row.total_received,
                'TCP': protocol_sizes.get('TCP', 0),
                'UDP': protocol_sizes.get('UDP', 0),
                'HTTP': protocol_sizes.get('HTTP', 0),
                'HTTPS': protocol_sizes.get('HTTPS', 0),
                'SSH': protocol_sizes.get('SSH', 0),
                'DNS': protocol_sizes.get('DNS', 0),
                'ICMP': protocol_sizes.get('ICMP', 0),
                'timestamp': row.timestamp
            })
    finally:
        # 关闭数据库会话
        session.close()

    # 返回数据的 DataFrame
    return pd.DataFrame(data)


# 加载数据
df = load_data()

# 提取特征
features = ['total_sent', 'total_received', 'TCP', 'UDP', 'HTTP', 'HTTPS', 'SSH', 'DNS', 'ICMP']

# 训练每个特征的 Isolation Forest 模型
models = {}
for feature in features:
    X = df[[feature]]
    model = IsolationForest(contamination=0.01, random_state=42)
    model.fit(X)
    models[feature] = model

# 保存模型
for feature, model in models.items():
    joblib.dump(model, f"{feature}_isolation_forest_model.joblib")

print("Models trained and saved.")
