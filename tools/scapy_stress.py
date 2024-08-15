from scapy.all import *

# 目标IP地址
target_ip = "49.232.245.103"

# 数据包的大小（字节）
packet_size = 1500  # Ethernet 最大传输单元(MTU)为1500字节

# 创建一个带有自定义负载的数据包
packet = IP(dst=target_ip) / ICMP() / Raw(load="X" * (packet_size - 28))  # IP头部20字节 + ICMP头部8字节 = 28字节

# 发送数据包的次数
num_packets = 1000

# 发送数据包
for _ in range(num_packets):
    send(packet)
    print(f"Sent packet with {packet_size} bytes to {target_ip}")
