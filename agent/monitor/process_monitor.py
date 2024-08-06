import time
import threading

import psutil

from agent.handler.exception_handler import exception_handler_for_class

@exception_handler_for_class
class ProcessMonitor:
    def __init__(self, callback, processes_to_monitor, interval=1):
        self.callback = callback
        self.processes_to_monitor = processes_to_monitor
        self.interval = interval
        self.running = False
        self.thread = threading.Thread(target=self.run)

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def run(self):
        previous_processes = {p.pid: p.info for p in psutil.process_iter(['pid', 'name'])}
        while self.running:
            time.sleep(self.interval)
            current_processes = {p.pid: p.info for p in psutil.process_iter(['pid', 'name'])}
            started = [p for p in current_processes.values() if p['name'] in self.processes_to_monitor and p['pid'] not in previous_processes]
            stopped = [p for p in previous_processes.values() if p['name'] in self.processes_to_monitor and p['pid'] not in current_processes]
            for process in started:
                self.callback('started', process['pid'])
            for process in stopped:
                self.callback('stopped', process['pid'])
            previous_processes = current_processes

