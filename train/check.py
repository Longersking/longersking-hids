import pandas as pd
import joblib
import json
from sklearn.preprocessing import StandardScaler

# 加载训练好的模型
models = {}
scalers = {}
features = ['total_sent', 'total_received', 'TCP', 'UDP', 'HTTP', 'HTTPS', 'SSH', 'DNS', 'ICMP']
for feature in features:
    models[feature] = joblib.load(f"{feature}_isolation_forest_model.joblib")

def detect_anomaly(data):
    protocol_sizes = json.loads(data["protocol_sizes"])
    df = pd.DataFrame([{
        'total_sent': data["total_sent"],
        'total_received': data["total_received"],
        'TCP': protocol_sizes.get("TCP", 0),
        'UDP': protocol_sizes.get("UDP", 0),
        'HTTP': protocol_sizes.get("HTTP", 0),
        'HTTPS': protocol_sizes.get("HTTPS", 0),
        'SSH': protocol_sizes.get("SSH", 0),
        'DNS': protocol_sizes.get("DNS", 0),
        'ICMP': protocol_sizes.get("ICMP", 0)
    }])

    # 计算每个字段的异常得分
    feature_scores = {}
    for feature in df.columns:
        model = models[feature]
        feature_data = df[[feature]]
        feature_score = model.decision_function(feature_data)[0]
        feature_scores[feature] = feature_score

    # 标准化得分
    scores = list(feature_scores.values())
    scaler = StandardScaler()
    scaled_scores = scaler.fit_transform(pd.DataFrame(scores).T)

    # 综合各个字段的异常得分
    total_score = scaled_scores.sum()

    # 判断是否为异常值
    threshold = -0.5  # 根据实际情况调整阈值
    if total_score < threshold:
        result = "Anomaly detected"
    else:
        result = "Normal traffic"

    return result, feature_scores, total_score

# 示例数据
sample_data = {
    "ip": "49.232.245.103",
    "total_sent": 19.1052,
    "total_received": 40.1041,
    "protocol_sizes": "{\"TCP\": 100.0007, \"UDP\": 10.0001, \"HTTP\": 0.0, \"HTTPS\": 0.0, \"SSH\": 0.0, \"DNS\": 0.0, \"ICMP\": 0.0001}",
    "timestamp": "2024-36-02 14:36:28"
}

# 检测
result, feature_scores, total_score = detect_anomaly(sample_data)
print("Result:", result)
print("Feature Scores:", feature_scores)
print("Total Score:", total_score)
