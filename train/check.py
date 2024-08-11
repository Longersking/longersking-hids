import pandas as pd
import joblib
import json


def detect_anomaly(data):
    ip = data["ip"]
    traffic_data = json.loads(data["data"])
    total_sent = traffic_data["total_sent"]
    total_received = traffic_data["total_received"]

    model_sent_file = f"models/{ip}_sent_isolation_forest_model.joblib"
    model_received_file = f"models/{ip}_received_isolation_forest_model.joblib"

    try:
        model_sent = joblib.load(model_sent_file)
        model_received = joblib.load(model_received_file)
    except FileNotFoundError:
        return f"No model found for IP: {ip}", {}, 0

    df_sent = pd.DataFrame([{'total_sent': total_sent}])
    df_received = pd.DataFrame([{'total_received': total_received}])

    # 预测是否为异常点
    is_anomaly_sent = model_sent.predict(df_sent)[0] == -1
    print(model_sent.predict(df_sent)[0])
    is_anomaly_received = model_received.predict(df_received)[0] == -1

    # 计算综合异常概率
    if is_anomaly_sent and is_anomaly_received:
        probability = 1.0  # 两个字段都异常，风险最高
        result = "Anomaly detected: High risk"
    elif is_anomaly_sent or is_anomaly_received:
        probability = 0.5  # 只有一个字段异常，风险中等
        result = "Anomaly detected: Moderate risk"
    else:
        probability = 0.0  # 两个字段都不异常，风险最低
        result = "Normal traffic"

    return result, {'total_sent': is_anomaly_sent, 'total_received': is_anomaly_received}, probability


# 示例数据
sample_data = {
    "ip": "121.43.132.126",
    "data": "{\"total_sent\": 3.3563, \"total_received\": 3.3874, \"protocol_sizes\": {\"TCP\": 0.0513, \"UDP\": 0.0019, \"HTTP\": 0.0, \"HTTPS\": 0.0471, \"SSH\": 0.0006, \"DNS\": 0.0019, \"ICMP\": 0.0}}",
    "type": "traffic_stats",
    "time": "2024-08-02 21:00:02"
}

# 检测
result, anomalies, probability = detect_anomaly(sample_data)
print("Result:", result)
print("Anomalies:", anomalies)
print("Probability:", probability)
