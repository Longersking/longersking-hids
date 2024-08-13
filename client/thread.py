from system_monitor import Monitor as SystemMonitor
import time
from handler.exception_handler import exception_handler
from monitor.process_monitor import ProcessMonitor
from monitor.file_monitor import FileMonitor  # 导入 file_monitor 模块
from handler.FIDS_handler import FIDShandler
from config import CRITICAL_PATHS, MONITORED_PATHS

def system_load_thread(queue, ip_address):
    monitor = SystemMonitor()
    while True:
        system_load = {
            'cpu': monitor.cpu(),
            'mem': monitor.mem(),
            'swap_memory': monitor.swap_memory(),
            'disk': monitor.disk(),
            'net': monitor.net(),
            'lastest_start_time': monitor.lastest_start_time(),
            'logined_users': monitor.logined_users(),
            'process_info': monitor.processes_info(),
        }
        queue.put(system_load)
        time.sleep(1)

@exception_handler
def process_monitor_thread(processes_to_monitor, queue):
    def process_callback(event_type, pid):
        print(event_type, pid)
    process_monitor = ProcessMonitor(process_callback, processes_to_monitor, queue)
    process_monitor.run()

def file_monitor_thread(alarm_queue, monitored_paths):
    fids_handler = FIDShandler(alarm_queue)
    monitor_paths = list(CRITICAL_PATHS.keys())
    monitor = FileMonitor(paths=monitor_paths, monitored_paths=monitored_paths, fids_handler=fids_handler)
    monitor.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop()

def file_monitor_callback(event_type, event_path):
    print(event_type, event_path)
