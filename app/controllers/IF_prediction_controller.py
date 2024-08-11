import pandas as pd
import joblib
import json

class IFPredictionController:
    def detect_sent_recv_risk(data):
        ip = data["ip"]
        traffic_data = json.loads(data["data"])
        total_sent = traffic_data["total_sent"]
        total_received = traffic_data["total_received"]

        model_sent_file = f"app/ml_models/{ip}_sent_isolation_forest_model.joblib"
        model_received_file = f"app/ml_models/{ip}_received_isolation_forest_model.joblib"

        try:
            model_sent = joblib.load(model_sent_file)
            model_received = joblib.load(model_received_file)
        except FileNotFoundError:
            return f"No model found for IP: {ip}", {}, 0

        df_sent = pd.DataFrame([{'total_sent': total_sent}])
        df_received = pd.DataFrame([{'total_received': total_received}])

        # 预测是否为异常点
        is_anomaly_sent = model_sent.predict(df_sent)[0] == -1
        is_anomaly_received = model_received.predict(df_received)[0] == -1

        # 计算综合异常概率
        if is_anomaly_sent and is_anomaly_received:
            return 1 # 两个字段都异常，认为存在风险
        else:
            return 0