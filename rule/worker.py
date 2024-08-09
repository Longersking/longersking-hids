import threading
from queue import Queue

class Worker:
    def __init__(self, packet_processor, num_threads=4):
        self.packet_queue = Queue()
        self.packet_processor = packet_processor
        self.num_threads = num_threads
        self.threads = []

    def start_workers(self):
        for _ in range(self.num_threads):
            t = threading.Thread(target=self.worker)
            t.start()
            self.threads.append(t)

    def worker(self):
        while True:
            packet = self.packet_queue.get()
            if packet is None:
                break
            self.packet_processor.process_packet(packet)
            self.packet_queue.task_done()

    def stop_workers(self):
        for _ in range(self.num_threads):
            self.packet_queue.put(None)
        for t in self.threads:
            t.join()

    def add_packet(self, packet):
        self.packet_queue.put(packet)

    def wait_for_completion(self):
        self.packet_queue.join()
