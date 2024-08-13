import json
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
from sqlalchemy import create_engine

model_dir = "cpu_models_20"
engine = create_engine('mysql+pymysql://username:password@host/dbname')


# 解析 JSON 数据并提取最大核心数
def parse_cpu_data(cpu_data):
    features = {
        'percent_avg': cpu_data['percent_avg']
    }
    for i, percent in enumerate(cpu_data['percent_per']):
        features[f'core_{i}_percent'] = percent
    return features, len(cpu_data['percent_per'])


# 补全缺失列
def complete_features(features, max_core):
    for i in range(max_core):
        if f'core_{i}_percent' not in features:
            features[f'core_{i}_percent'] = 0.0  # 用 0.0 填充缺失值
    return features


def load_model(ip):
    scaler = joblib.load(os.path.join(model_dir, f'{ip}_scaler.pkl'))
    lof = joblib.load(os.path.join(model_dir, f'{ip}_lof.pkl'))
    return scaler, lof


def detect_anomaly(ip, new_data, max_core):
    if not os.path.exists(os.path.join(model_dir, f'{ip}_scaler.pkl')) or not os.path.exists(
            os.path.join(model_dir, f'{ip}_lof.pkl')):
        raise ValueError(f"No model found for IP {ip}")

    # 加载模型
    scaler, lof = load_model(ip)

    # 解析新数据
    features, num_cores = parse_cpu_data(new_data)
    features = complete_features(features, max_core)
    X_new = pd.json_normalize(features)

    # 检查并填充 NaN 值
    X_new = X_new.fillna(0.0)

    # 标准化特征
    X_new_scaled = scaler.transform(X_new)

    # 预测是否为异常
    is_anomaly = lof.predict(X_new_scaled)

    return is_anomaly[0] == -1


def log_alert(ip, new_data, risk_level, risk_type, description):
    alert_data = {
        'type': risk_type,
        'level': risk_level,
        'ip': ip,
        'desc': description,
        'application': 'CPU Load Monitoring',
        'snapshot': new_data,
        'source_ip': None,
        'port': None,
        'target_ip': None,
        'target_port': None,
        'packet': None,
        'create_time': datetime.now()
    }

    alert_df = pd.DataFrame([alert_data])
    alert_df.to_sql('alert_log', engine, if_exists='append', index=False)


def evaluate_risk(features):
    avg_usage = features['percent_avg']
    core_usages = [features[f'core_{i}_percent'] for i in range(len(features) - 1)]  # 减去1是因为还有一个percent_avg

    # 评估风险等级
    if avg_usage > 90:
        risk_level = 'critical'
    elif avg_usage > 70:
        risk_level = 'high'
    elif avg_usage > 50:
        risk_level = 'medium'
    else:
        risk_level = 'low'

    reasons = []
    if avg_usage > 70:
        reasons.append("CPU使用率高，可能是由于密集的任务或恶意软件。")
    if any(core > 90 for core in core_usages):
        reasons.append("一个或多个内核负载过重，可能是由于特定的进程问题或有针对性的攻击。")
    else:
        reasons.append("异常的主从CPU占用比。")
    return risk_level, reasons


def handle_new_data(ip, new_data, max_core):
    features, num_cores = parse_cpu_data(new_data)
    features = complete_features(features, max_core)
    if detect_anomaly(ip, new_data, max_core):
        risk_level, reasons = evaluate_risk(features)
        description = "检测到CPU负载异常。可能的原因: " + "; ".join(reasons)
        print(description)
        # log_alert(ip, new_data, risk_level, 'CPU Anomaly', description)

def predict_cpu_load(data_json):
    data = json.loads(data_json['data'])
    # 获取 max_cores 数据
    data["cpu"].pop("cpu_times")
    max_cores = 8
    handle_new_data(data_json['ip'], data['cpu'], max_cores)
# 示例数据
str = r'{"ip": "121.43.132.126", "data": "{\"cpu\": {\"percent_avg\": 14.0, \"percent_per\": [28.1, 1.3, 30.1, 9.2, 27.3, 0.0, 16.2, 0.0], \"num_physic\": 4, \"num_logic\": 8, \"cpu_times\": {\"user\": 733747.13, \"system\": 12.37, \"idle\": 143720.81, \"interrupt\": 61946905.05, \"dead\": 41122.02}}, \"mem\": {\"total\": 7.37, \"used\": 2.86, \"free\": 0.12, \"percent\": 42.6}, \"swap_memory\": {\"total\": 0.0, \"used\": 0.0, \"free\": 0.0, \"percent\": 0.0}, \"disk\": [{\"device\": \"/dev/vda1\", \"mountpoint\": \"/\", \"fstype\": \"ext4\", \"opts\": \"rw,relatime,data=ordered\", \"used\": {\"total\": 492.03, \"used\": 267.19, \"free\": 204.62, \"percent\": 56.6}, \"io\": {\"read_mb_s\": 7.484375, \"write_mb_s\": 0.0, \"read_times_s\": 120, \"write_times_s\": 0}}], \"net\": [{\"name\": \"eth0\", \"bytes_sent\": 283762715396, \"bytes_recv\": 138253651777, \"packets_sent\": 120621538, \"packets_recv\": 186805900, \"family\": \"AF_INET\", \"address\": \"172.30.74.118\", \"netmask\": \"255.255.240.0\", \"broadcast\": \"172.30.79.255\"}, {\"name\": \"lo\", \"bytes_sent\": 775213027665, \"bytes_recv\": 775213027665, \"packets_sent\": 4568997141, \"packets_recv\": 4568997141, \"family\": \"AF_INET\", \"address\": \"127.0.0.1\", \"netmask\": \"255.0.0.0\", \"broadcast\": null}], \"lastest_start_time\": \"2024-05-08 13:59:16\", \"logined_users\": [], \"process_info\": {\"total_process_count\": 175, \"active_process_count\": 0, \"top_10_processes\": [{\"pid\": 1978, \"memory_percent\": 24.49217452662792, \"name\": \"mysqld\", \"cpu_percent\": 53.1}, {\"pid\": 19366, \"memory_percent\": 1.9968484971387126, \"name\": \"php-fpm\", \"cpu_percent\": 59.7}, {\"pid\": 26880, \"memory_percent\": 0.8021536993946341, \"name\": \"python3\", \"cpu_percent\": 2.6}, {\"pid\": 22817, \"memory_percent\": 0.888028531136869, \"name\": \"AliYunDunMonitor\", \"cpu_percent\": 1.3}, {\"pid\": 419, \"memory_percent\": 2.0597026661548665, \"name\": \"systemd-journald\", \"cpu_percent\": 0.0}, {\"pid\": 1237, \"memory_percent\": 1.0906620949527328, \"name\": \"rsyslogd\", \"cpu_percent\": 0.0}, {\"pid\": 20883, \"memory_percent\": 0.8720433967944891, \"name\": \"BT-Panel\", \"cpu_percent\": 0.0}, {\"pid\": 1986, \"memory_percent\": 0.09751449267115216, \"name\": \"redis-server\", \"cpu_percent\": 0.7}, {\"pid\": 68, \"memory_percent\": 0.0, \"name\": \"kswapd0\", \"cpu_percent\": 0.7}, {\"pid\": 21325, \"memory_percent\": 0.5255953557235575, \"name\": \"BT-Task\", \"cpu_percent\": 0.0}]}}", "type": "system_load", "time": "2024-08-07 18:11:06"}'
data_json = json.loads(str)
# 以上是dealWsData方法得到的数据

predict_cpu_load(data_json)
