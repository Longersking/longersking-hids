import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sklearn.ensemble import IsolationForest
import joblib
import sys
import os
import matplotlib.pyplot as plt

# 添加当前文件所在目录的父目录到 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import traffic_data
from app.config.base import mysql_username, mysql_password, mysql_host, mysql_port, mysql_db

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
                'timestamp': row.timestamp
            })
    finally:
        # 关闭数据库会话
        session.close()

    # 返回数据的 DataFrame
    return pd.DataFrame(data)




# 加载数据
df = load_data()

# 获取所有唯一的IP地址
ips = df['ip'].unique()

# 创建 models 目录
os.makedirs('net_models', exist_ok=True)

# 为每个IP地址训练Isolation Forest模型
# ips=["49.232.245.103"]
# ips=["121.43.132.126"]
for ip in ips:
    ip_data_sent = df[df['ip'] == ip][['total_sent']]
    ip_data_received = df[df['ip'] == ip][['total_received']]
    print(ip_data_received['total_received'])
    plt.scatter(ip_data_received['total_received'], ip_data_sent['total_sent'])
    plt.show()

    model_sent = IsolationForest(random_state=42)
    model_sent.fit(ip_data_sent)
    joblib.dump(model_sent, f"net_models/{ip}_sent_isolation_forest_model.joblib")

    model_received = IsolationForest(contamination=0.01, random_state=42)
    model_received.fit(ip_data_received)
    joblib.dump(model_received, f"net_models/{ip}_received_isolation_forest_model.joblib")

print("Models trained and saved for each IP.")
