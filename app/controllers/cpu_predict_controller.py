import json
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
from sqlalchemy import create_engine
from app.models.base import SessionLocal

model_dir = "app/ml_models/lof_cpu"
db = SessionLocal()


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


def evaluate_risk(features):
    avg_usage = features['percent_avg']
    core_usages = [features[f'core_{i}_percent'] for i in range(len(features) - 1)]  # 减去1是因为还有一个percent_avg

    # 评估风险等级
    if avg_usage > 90:
        risk_level = 'critical'
    elif avg_usage > 70:
        risk_level = 'serious'
    elif avg_usage > 50:
        risk_level = 'medium'
    else:
        risk_level = 'light'

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
    res = detect_anomaly(ip, new_data, max_core)
    if (res and features['percent_avg'] > 20) or features['percent_avg'] > 80:
        risk_level, reasons = evaluate_risk(features)
        description = "检测到CPU负载异常。可能的原因: " + "; ".join(reasons)
        return 1, risk_level, description
    else:
        return 0, "",""


def predict_cpu_load(data_json):
    data = json.loads(data_json['data'])
    # 获取 max_cores 数据
    data["cpu"].pop("cpu_times")
    max_cores = 8
    res, risk_level, description = handle_new_data(data_json['ip'], data['cpu'], max_cores)
    return res, risk_level, description
