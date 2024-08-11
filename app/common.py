import json
from app.controllers.traffic_controller import insert_traffic_data
from app.controllers.IF_prediction_controller import IFPredictionController
from app.controllers.alert_controller import write_alert
from app.controllers.system_load_controller import insert_system_load
from app.controllers.cpu_predict_controller import predict_cpu_load
from app.controllers.process_monitor_controller import deal_process_monitor
from app.controllers.file_monitor_controller import deal_file_alarms, record_file_change
from app.controllers.packet_moniter_controller import process_packet_data
def dataReturn(code: int, msg: str | int, data=None):
    if data is not None:
        return {'code': code, 'msg': msg, 'data': data}
    else:
        return {'code': code, 'msg': msg, 'data': data}

def dealWsData(data_json):
    if data_json['type'] == "traffic_stats":
        try:
            # 插入流量记录
            # insert_traffic_data(data_json)
            # 预测攻击
            res = IFPredictionController.detect_sent_recv_risk(data_json)
            if res == 1:
                # 记录轻微告警
                desc = """
一秒内出入网流量同时过高！
出网带宽:{0}MBPS
入网带宽:{1}MBPS
可能的原因：恶意下载/上传文件
                """.format(json.loads(data_json['data'])['total_sent'],json.loads(data_json['data'])['total_received'])
                write_alert(type="traffic_alert", level="light", ip=data_json['ip'], desc=desc, snapshot=data_json['data'])
        except Exception as e:
            print(f"insert traffic data error: {e}")
    elif data_json['type'] == "system_load":
        try:
            # 预测CPU异常
            res, level, desc = predict_cpu_load(data_json)
            if res:
                write_alert(type="cpu_load_alert", level=level, ip=data_json['ip'], desc=desc, snapshot=data_json['data'])
            # 写入系统负载记录
            # insert_system_load(data_json)
        except Exception as e:
            print(f"system_load write error {e}")
    elif data_json['type'] == "process_data":
        # 处理进程监控
        try:
            deal_process_monitor(data_json)
        except Exception as e:
            print(f"process_data write error {e}")
    elif data_json['type'] == "file_change":
        try:
            data = json.loads(data_json['data'])
            if data.get('type') == 'alarms':
                deal_file_alarms(data_json)
            else:
                record_file_change(data_json)
        except Exception as e:
            print(f"file_change write error {e}")
    elif data_json['type'] == "packet_monitor":
        try:
            process_packet_data(data_json)
        except Exception as e:
            print(f"file_change write error {e}")
