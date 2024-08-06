import threading

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from agent.handler.exception_handler import exception_handler_for_class

# 文件监视器
@exception_handler_for_class
class FileMonitorHandler(FileSystemEventHandler):
    """
        file monitor handler
        params:
            callback: callback function
            event: event object
        return:
            None
    """
    def __init__(self, callback):
        self.callback = callback

    def on_modified(self, event):
        self.callback('modified', event.src_path)

    def on_created(self, event):
        self.callback('created', event.src_path)

    def on_deleted(self, event):
        self.callback('deleted', event.src_path)

class FileMonitor:
    """
       file monitor
       params:
           paths: file path lists what you want to monitor
           callback: callback function
       return:
           None
       exception:
           file not found and not exist
    """
    def __init__(self, paths: str, callback):
        self.paths = paths
        self.callback = callback
        self.event_handler = FileMonitorHandler(callback)
        self.observers = []

    def start(self):
        for path in self.paths:
            observer = Observer()
            observer.schedule(self.event_handler, path, recursive=True)
            observer.start()
            self.observers.append(observer)
        self._run_observers()

    def _run_observers(self):
        for observer in self.observers:
            thread = threading.Thread(target=observer.join)
            thread.start()

    def stop(self):
        for observer in self.observers:
            observer.stop()
            observer.join()
