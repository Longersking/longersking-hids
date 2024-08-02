import psutil
import time
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.all import sniff

# 存储各协议的数据包大小
protocol_sizes = {
    'TCP': 0,
    'UDP': 0,
    'HTTP': 0,
    'HTTPS': 0,
    'SSH': 0,
    'DNS': 0,
    'ICMP': 0
}

# 定义协议的端口
HTTP_PORTS = [80, 8080]
HTTPS_PORTS = [443]
SSH_PORTS = [22]
DNS_PORTS = [53]


# 捕获数据包并统计大小
def packet_callback(packet):
    global protocol_sizes

    if packet.haslayer(IP):
        ip_layer = packet.getlayer(IP)
        packet_size = len(packet)

        if packet.haslayer(TCP):
            protocol_sizes['TCP'] += packet_size
            tcp_layer = packet.getlayer(TCP)
            if tcp_layer.dport in HTTP_PORTS or tcp_layer.sport in HTTP_PORTS:
                protocol_sizes['HTTP'] += packet_size
            elif tcp_layer.dport in HTTPS_PORTS or tcp_layer.sport in HTTPS_PORTS:
                protocol_sizes['HTTPS'] += packet_size
            elif tcp_layer.dport in SSH_PORTS or tcp_layer.sport in SSH_PORTS:
                protocol_sizes['SSH'] += packet_size

        elif packet.haslayer(UDP):
            protocol_sizes['UDP'] += packet_size
            udp_layer = packet.getlayer(UDP)
            if udp_layer.dport in DNS_PORTS or udp_layer.sport in DNS_PORTS:
                protocol_sizes['DNS'] += packet_size

        elif packet.haslayer(ICMP):
            protocol_sizes['ICMP'] += packet_size


# 每秒打印流量信息
def monitor_traffic():
    global protocol_sizes

    # 获取初始的网络I/O统计信息
    net_io_initial = psutil.net_io_counters()

    while True:
        # 捕获数据包
        sniff(prn=packet_callback, store=0, timeout=1)

        # 获取当前的网络I/O统计信息
        net_io_current = psutil.net_io_counters()

        # 计算流入和流出流量（单位：Mb/s）
        bytes_sent_per_sec = (net_io_current.bytes_sent - net_io_initial.bytes_sent) / 1024 / 1024
        bytes_recv_per_sec = (net_io_current.bytes_recv - net_io_initial.bytes_recv) / 1024 / 1024

        print(f"Total Traffic: Sent: {bytes_sent_per_sec:.2f} Mb/s, Received: {bytes_recv_per_sec:.2f} Mb/s")

        # 打印各协议的数据包大小
        for protocol, size in protocol_sizes.items():
            print(f"{protocol}: {size / 1024 / 1024:.2f} MB")

        # 重置统计数据
        protocol_sizes = {key: 0 for key in protocol_sizes}

        # 更新初始网络I/O统计信息
        net_io_initial = net_io_current

        # 每秒获取一次数据
        time.sleep(0.1)


if __name__ == "__main__":
    monitor_traffic()
