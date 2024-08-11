from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from handler.FIDS_handler import FIDShandler
import os
import logging

# 文件监控事件处理器
class FileMonitorHandler(FileSystemEventHandler):
    def __init__(self, fids_handler):
        self.fids_handler = fids_handler

    def on_modified(self, event):
        self.fids_handler.check_event(event)

    def on_created(self, event):
        self.fids_handler.check_event(event)

    def on_deleted(self, event):
        self.fids_handler.check_event(event)

# 文件监控类
class FileMonitor:
    def __init__(self, paths, monitored_paths, fids_handler):
        self.paths = paths
        self.monitored_paths = monitored_paths
        self.fids_handler = fids_handler
        self.event_handler = FileMonitorHandler(fids_handler)
        self.observers = []

    def start(self):
        for path in self.paths + self.monitored_paths:
            if not os.path.exists(path):
                logging.error(f"监控路径不存在: {path}")
                continue
            if not os.access(path, os.R_OK):
                logging.error(f"无读取权限: {path}")
                continue
            observer = Observer()
            observer.schedule(self.event_handler, path, recursive=True)
            observer.start()  # 确保 observer 被启动
            self.observers.append(observer)

    def stop(self):
        for observer in self.observers:
            observer.stop()
            observer.join()
