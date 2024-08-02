import asyncio
import time

from scapy.all import sniff
from scapy.layers.inet import IP
from .utils import get_ip_address
from .websocket_client import send_packet_data

def packet_callback(packet):
    protocol = packet.sprintf("{IP:%IP.proto%}").lower()
    if protocol == "tcp":
        protocol = "TCP"
    elif protocol == "udp":
        protocol = "UDP"
    elif protocol == "icmp":
        protocol = "ICMP"
    elif protocol == "http":
        protocol = "HTTP"
    elif protocol == "https":
        protocol = "HTTPS"
    else:
        protocol = "OTHER"

    packet_size = len(packet)
    direction = "out" if IP in packet and packet[IP].src == get_ip_address() else "in"

    stats = {
        'ip': get_ip_address(),
        'protocol': protocol,
        'packet_size': packet_size,
        'direction': direction,
        'time': time.strftime("%H:%M:%S", time.localtime())
    }
    asyncio.run(send_packet_data(stats))

def start_sniffing():
    sniff(prn=packet_callback, store=0)
