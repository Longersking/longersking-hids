# 文件路径: /mnt/data/capture.py

from scapy.all import sniff
from scapy.layers.inet import IP
import threading

class TrafficCapture:
    def __init__(self, interface):
        self.interface = interface

    def process_packet(self, packet):
        if IP in packet:
            ip_layer = packet[IP]
            src_ip = ip_layer.src
            dst_ip = ip_layer.dst
            proto = ip_layer.proto

            if proto == 6:  # TCP协议
                protocol = "TCP"
            elif proto == 17:  # UDP协议
                protocol = "UDP"
            else:
                protocol = "Other"

            traffic_size = len(packet)

            print(f"Interface: {self.interface}, Source IP: {src_ip}, Destination IP: {dst_ip}, Protocol: {protocol}, Traffic Size: {traffic_size} bytes")

    def start_capture(self):
        try:
            sniff(iface=self.interface, prn=self.process_packet, store=0)
        except Exception as e:
            print(f"Error capturing on interface {self.interface}: {e}")

def start_capture_on_interface(interface):
    capture = TrafficCapture(interface)
    capture.start_capture()

def capture_on_interfaces(interfaces):
    threads = []
    for interface in interfaces:
        thread = threading.Thread(target=start_capture_on_interface, args=(interface,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

