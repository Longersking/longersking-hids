import time
from multiprocessing import Process
import threading

from websocket_client import WebSocketClient

import config
from agent.monitor.file_monitor import FileMonitor
from agent.monitor.process_monitor import ProcessMonitor
from agent.monitor.sys_monitor import SysMonitor
from agent.handler.exception_handler import exception_handler

# 创建一个全局锁
lock = threading.Lock()

def dataReturn(code: int, msg: str, data=None) -> dict:
    """
    Return data format
    params:
        code:
        msg:
        data:
    returns:
        code:
        msg:
        data:
    """
    return {'code': code, 'msg': msg, 'data': data}

@exception_handler
def send_data(uri: str, message: str):
    with lock:  # 使用全局锁确保线程安全
        ws_client = WebSocketClient(uri)
        ws_client.connect()
        ws_client.send_message(message)
        ws_client.close()

@exception_handler
def monitor_sys(uri: str):
    ws_client = WebSocketClient(uri)
    ws_client.connect()
    sys_monitor = SysMonitor()
    try:
        while True:
            cpu_data = sys_monitor.cpu()
            mem_data = sys_monitor.mem()
            net_data = sys_monitor.net()
            send_data(uri, dataReturn(1, "Monitoring data", {"type": "system", "cpu": cpu_data, "memory": mem_data, "network": net_data}))
            time.sleep(5)
    except KeyboardInterrupt:
        pass
    finally:
        ws_client.close()

@exception_handler
def monitor_files(uri: str, paths: list):
    def file_callback(event_type, path: str):
        send_data(uri, dataReturn(1, "Monitoring data", {"type": "file", "event": event_type, "path": path}))

    file_monitor = FileMonitor(paths, file_callback)
    file_monitor.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        file_monitor.stop()

@exception_handler
def monitor_processes(uri: str, processes_to_monitor):
    def process_callback(event_type, pid):
        send_data(uri, dataReturn(1, "Monitoring data", {"type": "process", "event": event_type, "pid": pid}))

    process_monitor = ProcessMonitor(process_callback, processes_to_monitor)
    process_monitor.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        process_monitor.stop()

@exception_handler
def start_monitoring(file_uri: str, sys_uri: str, process_uri: str, paths: list, processes_to_monitor):
    # Create processes for each monitor
    if paths and processes_to_monitor:
        file_process = Process(target=monitor_files, args=(file_uri, paths))
        process_monitor_process = Process(target=monitor_processes, args=(process_uri, processes_to_monitor))
        sys_process = Process(target=monitor_sys, args=(sys_uri,))

        # Start processes
        file_process.start()
        process_monitor_process.start()
        sys_process.start()

        # Wait for processes to complete
        file_process.join()
        process_monitor_process.join()
        sys_process.join()
    else:
        print("No monitor to start")

if __name__ == "__main__":
    server_base_uri = "ws://192.168.100.101:8004/test"
    file_uri = f"{server_base_uri}/files_info"
    sys_uri = f"{server_base_uri}/sys_info"
    process_uri = f"{server_base_uri}/processes_info"
    paths_to_monitor = config.get_config()["paths_to_monitor"]
    processes_to_monitor = config.get_config()["process_to_monitor"]

    start_monitoring(file_uri, sys_uri, process_uri, paths_to_monitor, processes_to_monitor)
