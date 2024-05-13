from scapy.layers.inet import IP, TCP, UDP
from scapy.packet import Packet

def parse_packet(packet: Packet):
    # 解析关键信息
    parsed_data = {}

    # 检查是否存在IP层
    if IP in packet:
        ip_layer = packet[IP]
        parsed_data["src_ip"] = ip_layer.src
        parsed_data["dst_ip"] = ip_layer.dst
        parsed_data["protocol"] = ip_layer.proto
    else:
        # 如果没有IP层，可能是其他类型的数据包
        parsed_data["src_ip"] = None
        parsed_data["dst_ip"] = None
        parsed_data["protocol"] = None

    # 检查是否存在TCP层
    if TCP in packet:
        tcp_layer = packet[TCP]
        parsed_data["src_port"] = tcp_layer.sport
        parsed_data["dst_port"] = tcp_layer.dport
    # 如果没有TCP层，检查UDP层
    elif UDP in packet:
        udp_layer = packet[UDP]
        parsed_data["src_port"] = udp_layer.sport
        parsed_data["dst_port"] = udp_layer.dport
    else:
        parsed_data["src_port"] = None
        parsed_data["dst_port"] = None

    # 添加数据包摘要
    parsed_data["summary"] = packet.summary()

    return parsed_data
