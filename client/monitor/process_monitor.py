import json
import time
import psutil
from handler.exception_handler import exception_handler_for_class


@exception_handler_for_class
class ProcessMonitor:
    def __init__(self, callback, processes_to_monitor, queue, interval=3):
        self.callback = callback
        self.processes_to_monitor = processes_to_monitor if processes_to_monitor else []
        self.interval = interval
        self.queue = queue

    def run(self):
        previous_processes = {p.pid: p.info for p in psutil.process_iter(
            ['pid', 'name', 'num_threads', 'status', 'memory_info', 'cpu_percent'])}
        print("进程监控线程开始运行")
        while True:
            time.sleep(self.interval)
            current_processes = {p.pid: p.info for p in psutil.process_iter(
                ['pid', 'name', 'num_threads', 'status', 'memory_info', 'cpu_percent'])}

            started = [p for p in current_processes.values() if
                       p['name'] in self.processes_to_monitor and p['pid'] not in previous_processes]
            stopped = [p for p in previous_processes.values() if
                       p['name'] in self.processes_to_monitor and p['pid'] not in current_processes]

            # 按CPU使用量倒序排序
            sorted_processes = sorted(current_processes.values(), key=lambda x: x['cpu_percent'], reverse=True)

            # 加入队列
            self.queue.put({
                "sorted_processes": sorted_processes,
                "started": started,
                "stopped": stopped,
                "started_num": len(started),
                "stopped_num": len(stopped)
            })

            previous_processes = current_processes
