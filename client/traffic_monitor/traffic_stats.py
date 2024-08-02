from utils import get_ip_address
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.all import sniff
import psutil
import time


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

def get_protocol_size(packet):
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
            
def deal_stats(queue,pos):
    global protocol_sizes

    # 获取初始的网络I/O统计信息
    net_io_initial = psutil.net_io_counters()
    while True:
        # 捕获数据包
        sniff(prn=get_protocol_size, store=0, timeout=1)

        # 获取当前的网络I/O统计信息
        net_io_current = psutil.net_io_counters()

        # 计算流入和流出流量（单位：Mb/s）
        bytes_sent_per_sec = (net_io_current.bytes_sent - net_io_initial.bytes_sent) 
        bytes_recv_per_sec = (net_io_current.bytes_recv - net_io_initial.bytes_recv) 

        # print(f"Total Traffic: Sent: {bytes_sent_per_sec:.2f} Mb/s, Received: {bytes_recv_per_sec:.2f} Mb/s")
        # 写入队列
        put_queue(queue,bytes_sent_per_sec,bytes_recv_per_sec,protocol_sizes)
        # 重置统计数据
        protocol_sizes = {key: 0 for key in protocol_sizes}

        # 更新初始网络I/O统计信息
        net_io_initial = net_io_current
        
        
        
        # 每秒获取一次数据
        time.sleep(1)
        
def put_queue(queue,bytes_sent_per_sec,bytes_recv_per_sec,protocol_sizes):
        data = {
            "total_sent": round(bytes_sent_per_sec / (1024 * 1024), 4),
            "total_received": round(bytes_recv_per_sec / (1024 * 1024), 4),
            "protocol_sizes": {k: round(v / (1024 * 1024), 4) for k, v in protocol_sizes.items()}
        } 
        queue.put(data)
        
        
            

class TrafficStats:
    def __init__(self):
        self.total_sent = 0
        self.total_received = 0
        self.protocol_sizes = {
            'TCP': 0,
            'UDP': 0,
            'HTTP': 0,
            'HTTPS': 0,
            'SSH': 0,
            'DNS': 0,
            'ICMP': 0
        }
        # 获取初始的网络I/O统计信息
        self.net_io_initial = psutil.net_io_counters()

    def update_stats(self, packet):
        # 定义协议的端口
        HTTP_PORTS = [80, 8080]
        HTTPS_PORTS = [443]
        SSH_PORTS = [22]
        DNS_PORTS = [53]
        
        if packet.haslayer(IP):
            ip_layer = packet.getlayer(IP)
            packet_size = len(packet)
            
            if packet.haslayer(TCP):
                self.protocol_sizes['TCP'] += packet_size
                tcp_layer = packet.getlayer(TCP)
                if tcp_layer.dport in HTTP_PORTS or tcp_layer.sport in HTTP_PORTS:
                    self.protocol_sizes['HTTP'] += packet_size
                elif tcp_layer.dport in HTTPS_PORTS or tcp_layer.sport in HTTPS_PORTS:
                    self.protocol_sizes['HTTPS'] += packet_size
                elif tcp_layer.dport in SSH_PORTS or tcp_layer.sport in SSH_PORTS:
                    self.protocol_sizes['SSH'] += packet_size
            elif packet.haslayer(UDP):
                self.protocol_sizes['UDP'] += packet_size
                udp_layer = packet.getlayer(UDP)
                if udp_layer.dport in DNS_PORTS or udp_layer.sport in DNS_PORTS:
                    self.protocol_sizes['DNS'] += packet_size
            elif packet.haslayer(ICMP):
                self.protocol_sizes['ICMP'] += packet_size
                
        
        # 获取当前的网络I/O统计信息
        net_io_current = psutil.net_io_counters()

        # 计算并更新发送和接收的总数据量，单位：字节
        self.bytes_sent_per_sec = (net_io_current.bytes_sent - self.net_io_initial.bytes_sent) 
        self.bytes_recv_per_sec = (net_io_current.bytes_recv - self.net_io_initial.bytes_recv)
        
        # 更新初始网络I/O统计信息
        self.net_io_initial = net_io_current
        # 重置统计数据
        self.protocol_sizes = {key: 0 for key in self.protocol_sizes}

        

    def get_current_stats(self):
        return {
            "total_sent": round(self.bytes_sent_per_sec / (1024 * 1024), 4),
            "total_received": round(self.bytes_recv_per_sec / (1024 * 1024), 4),
            "protocol_sizes": {k: round(v / (1024 * 1024), 4) for k, v in self.protocol_sizes.items()}
        }
        
    def reset_stats(self):
        self.total_sent = 0
        self.total_received = 0
        self.protocol_sizes = {k: 0 for k in self.protocol_sizes}
        
    # 写入队列
    def writeQueue(sele,queue):
        pass
        
