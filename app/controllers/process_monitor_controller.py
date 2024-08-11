from typing import List, Dict, Any
from .alert_controller import write_alert
import json
from datetime import datetime
import numpy as np

# 保存上一次的进程信息
previous_process_data: Dict[str, Dict[int, Dict[str, Any]]] = {}
# 保存滑动窗口数据
window_data: Dict[str, Dict[int, List[Dict[str, Any]]]] = {}

# 记录警告
def log_alert(ip, data, prev_data, alert_type, level, description):
    alert_data = {
        'type': alert_type,
        'level': level,
        'ip': ip,
        'desc': description,
        'application': data.get('name', 'Unknown'),
        'snapshot': json.dumps({"current": data, "previous": prev_data}),
        'source_ip': None,
        'port': None,
        'target_ip': None,
        'target_port': None,
        'packet': None,
        'create_time': datetime.now()
    }
    write_alert(**alert_data)
    print(f"Alert logged: {alert_data}")

def process_alert_detect(ip, current_data, previous_data):
    current_processes = current_data['sorted_processes']
    started_num = current_data['started_num']

    if ip not in window_data:
        window_data[ip] = {}

    # 检查每个进程的资源使用情况
    for process in current_processes:
        pid = process["pid"]
        if pid not in window_data[ip]:
            window_data[ip][pid] = []

        window_data[ip][pid].append(process)

        if len(window_data[ip][pid]) > 30:  # 只保留最新的30条数据
            window_data[ip][pid].pop(0)

        if pid in previous_data:
            prev_process = previous_data[pid]
            window = window_data[ip][pid]

            if len(window) > 1:  # 确保有足够的数据点进行计算
                # 计算CPU标准差
                cpu_percents = [p['cpu_percent'] for p in window if 'cpu_percent' in p]
                if cpu_percents:
                    cpu_mean = np.mean(cpu_percents)
                    cpu_std = np.std(cpu_percents)
                    if cpu_std > 0 and prev_process["cpu_percent"] > 0:  # 确保标准差不是0且前一个值不为0
                        if process["cpu_percent"] > cpu_mean + 5 * cpu_std:
                            log_alert(ip, process, prev_process, "process_alert", "light",
                                      f"进程{pid} ({process['name']}) CPU使用率异常飙升超过5倍标准方差")
                        elif process["cpu_percent"] > cpu_mean + 8 * cpu_std:
                            log_alert(ip, process, prev_process, "process_alert", "medium",
                                      f"进程{pid} ({process['name']}) CPU使用率异常飙升超过8倍标准方差")
                        elif process["cpu_percent"] > cpu_mean + 15 * cpu_std:
                            log_alert(ip, process, prev_process, "process_alert", "serious",
                                      f"进程{pid} ({process['name']}) CPU使用率异常飙升超过15倍标准方差")
                        elif process["cpu_percent"] > cpu_mean + 20 * cpu_std:
                            log_alert(ip, process, prev_process, "process_alert", "critical",
                                      f"进程{pid} ({process['name']}) CPU使用率异常飙升超过20倍标准方差")

                # 计算内存标准差
                mem_usages = [p['memory_info'][1] for p in window if isinstance(p['memory_info'], list)]
                if mem_usages:
                    mem_mean = np.mean(mem_usages)
                    mem_std = np.std(mem_usages)
                    if mem_std > 0 and prev_process["memory_info"][1] > 0:  # 确保标准差不是0且前一个值不为0
                        if process["memory_info"][1] > mem_mean + 5 * mem_std:
                            log_alert(ip, process, prev_process, "process_alert", "light",
                                      f"进程{pid} ({process['name']}) 内存使用量异常飙升超过5倍标准方差")
                        elif process["memory_info"][1] > mem_mean + 8 * mem_std:
                            log_alert(ip, process, prev_process, "process_alert", "medium",
                                      f"进程{pid} ({process['name']}) 内存使用量异常飙升超过8倍标准方差")
                        elif process["memory_info"][1] > mem_mean + 15 * mem_std:
                            log_alert(ip, process, prev_process, "process_alert", "serious",
                                      f"进程{pid} ({process['name']}) 内存使用量异常飙升超过15倍标准方差")
                        elif process["memory_info"][1] > mem_mean + 20 * mem_std:
                            log_alert(ip, process, prev_process, "process_alert", "critical",
                                      f"进程{pid} ({process['name']}) 内存使用量异常飙升超过20倍标准方差")

                # 计算线程数标准差
                thread_counts = [p['num_threads'] for p in window if 'num_threads' in p]
                if thread_counts:
                    thread_mean = np.mean(thread_counts)
                    thread_std = np.std(thread_counts)
                    if thread_std > 0 and prev_process["num_threads"] > 0:  # 确保标准差不是0且前一个值不为0
                        if process["num_threads"] > thread_mean + 5 * thread_std:
                            log_alert(ip, process, prev_process, "process_alert", "light",
                                      f"进程{pid} ({process['name']}) 线程数异常增长超过5倍标准方差")
                        elif process["num_threads"] > thread_mean + 8 * thread_std:
                            log_alert(ip, process, prev_process, "process_alert", "medium",
                                      f"进程{pid} ({process['name']}) 线程数异常增长超过8倍标准方差")
                        elif process["num_threads"] > thread_mean + 15 * thread_std:
                            log_alert(ip, process, prev_process, "process_alert", "serious",
                                      f"进程{pid} ({process['name']}) 线程数异常增长超过15倍标准方差")
                        elif process["num_threads"] > thread_mean + 20 * thread_std:
                            log_alert(ip, process, prev_process, "process_alert", "critical",
                                      f"进程{pid} ({process['name']}) 线程数异常增长超过20倍标准方差")

    # 检查进程启动数
    if len(previous_data) * 0.2 < started_num <= len(previous_data) * 0.3:  # 阈值设为20%
        log_alert(ip, current_data, previous_data, "process_alert", "light", "进程启动增长数超出阈值（20%）")
    elif len(previous_data) * 0.3 < started_num <= len(previous_data) * 0.5:
        log_alert(ip, current_data, previous_data, "process_alert", "medium", "进程启动增长数超出阈值（30%）")
    elif started_num > len(previous_data) * 0.5:
        log_alert(ip, current_data, previous_data, "process_alert", "serious", "进程启动增长数超出阈值（50%）")

    # 检查进程唤醒数
    awake_processes = [p for p in current_processes if p["status"] == "running"]
    prev_awake_processes = [p for p in previous_data.values() if p["status"] == "running"]
    if len(prev_awake_processes) > 0 and len(awake_processes) > len(prev_awake_processes) * 1.5:
        log_alert(ip, awake_processes, prev_awake_processes, "process_alert", "medium", "进程唤醒数异常增加！")

def deal_process_monitor(data_json):
    ip = data_json['ip']
    data = json.loads(data_json['data'])
    if ip in previous_process_data:
        process_alert_detect(ip, data, previous_process_data[ip])
        print(f"{ip}的进程检查完毕！")
    previous_process_data[ip] = {proc["pid"]: proc for proc in data['sorted_processes']}
