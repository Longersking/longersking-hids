from scapy.all import sniff, IP, TCP, UDP, ICMP
from .traffic_stats import TrafficStats

class TrafficSniffer:
    def __init__(self):
        pass

    def sniff_packets(self, duration=1,callback=None):
        sniff(prn=callback,store=0,timeout=duration)

    def process_packets(self, packets):
        processed_packets = []
        for packet in packets:
            packet_info = {
                "src": packet[IP].src if packet.haslayer(IP) else None,
                "dst": packet[IP].dst if packet.haslayer(IP) else None,
                "proto": None,
                "size": len(packet)
            }
            if packet.haslayer(TCP):
                packet_info["proto"] = "TCP"
            elif packet.haslayer(UDP):
                packet_info["proto"] = "UDP"
            elif packet.haslayer(ICMP):
                packet_info["proto"] = "ICMP"

            processed_packets.append(packet_info)
        return processed_packets
