import scapy.all as scapy

class PacketParser:
    def parse_packet(self, packet):
        if packet.haslayer(scapy.IP):
            return {
                'src_ip': packet[scapy.IP].src,
                'dst_ip': packet[scapy.IP].dst,
                'protocol': packet[scapy.IP].proto,
                'payload': str(packet[scapy.IP].payload)
            }
        return {}
