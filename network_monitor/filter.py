import threading
import queue
import scapy.all as scapy

class PacketCapture:
    def __init__(self, interface, packet_queue):
        self.interface = interface
        self.packet_queue = packet_queue

    def packet_handler(self, packet):
        # 复制数据包
        packet_copy = packet.copy()
        self.packet_queue.put(packet_copy)
        # 释放原数据包
        del packet

    def start_capture(self):
        scapy.sniff(iface=self.interface, prn=self.packet_handler, store=False)

def start_capture_thread(interface, packet_queue):
    capture = PacketCapture(interface, packet_queue)
    capture_thread = threading.Thread(target=capture.start_capture)
    capture_thread.start()
    return capture_thread
