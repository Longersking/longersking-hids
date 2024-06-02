from scapy.all import sniff, wrpcap
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.http import HTTPRequest, HTTPResponse

from host_detection import sys_monitor

def get_all_interfaces():
    """获取所有网络接口名称"""
    m = sys_monitor.Monitor().net()
    return [net_name["name"] for net_name in m ]


def packet_handler(packet, iface):
    """处理捕捉到的数据包并提取和显示详细信息"""
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst

        if packet.haslayer(TCP):
            proto_type = "TCP"
        elif packet.haslayer(UDP):
            proto_type = "UDP"
        else:
            proto_type = "Other"

        # 提取HTTP/HTTPS数据包
        if packet.haslayer(HTTPRequest) or packet.haslayer(HTTPResponse):
            app_proto = "HTTP"
        else:
            app_proto = "Other"

        # 打印格式化输出
        packet_info = packet.summary()
        print(
            f"Interface: {iface}, Source IP: {ip_src}, Destination IP: {ip_dst}, Protocol: {proto_type}, App Protocol: {app_proto}, Packet Info: {packet_info}")

        # 保存数据包为pcap文件
        wrpcap(f"{iface}_captured_packets.pcap", [packet], append=True)


def start_sniffing(interface):
    """初始化捕捉器并开始捕捉数据包"""
    print(f"Starting packet capture on interface {interface}...")
    sniff(iface=interface, prn=lambda packet: packet_handler(packet, interface), store=False)


if __name__ == "__main__":
    # 获取所有网络接口
    interfaces = get_all_interfaces()
    print(interfaces)

    start_sniffing("WLAN")
    # 在每个接口上启动捕捉
    # for iface in interfaces:
    #     try:
    #         start_sniffing(iface)
    #     except Exception as e:
    #         print(f"Error starting capture on interface {iface}: {e}")
