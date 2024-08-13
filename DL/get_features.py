import psutil
from scapy.all import sniff, IP, TCP, UDP
import time
import statistics
import threading
import json
# 全局变量，用于存储实时网络流量特征
metrics = {
    'Flow Duration': 0,
    'Total Fwd Packets': 0,
    'Total Backward Packets': 0,
    'Fwd Packet Length Mean': 0,
    'Bwd Packet Length Mean': 0,
    'Flow Bytes/s': 0,
    'Flow Packets/s': 0,
    'Fwd IAT Mean': 0,
    'Bwd IAT Mean': 0,
    'Fwd PSH Flags': 0,
    'Bwd PSH Flags': 0,
    'Fwd URG Flags': 0,
    'Bwd URG Flags': 0,
    'Fwd Header Length': 0,
    'Bwd Header Length': 0,
    'Fwd Packets/s': 0,
    'Bwd Packets/s': 0,
    'Packet Length Std': 0,
    'Packet Length Variance': 0,
    'FIN Flag Count': 0,
    'SYN Flag Count': 0,
    'RST Flag Count': 0,
    'PSH Flag Count': 0,
    'ACK Flag Count': 0,
    'URG Flag Count': 0,
    'CWE Flag Count': 0,
    'ECE Flag Count': 0,
    'Down/Up Ratio': 0,
    'Average Packet Size': 0,
    'Fwd Segment Size Avg': 0,
    'Bwd Segment Size Avg': 0,
    'FWD Init Win Bytes': 0,
    'Bwd Init Win Bytes': 0,
    'Fwd Act Data Pkts': 0
}

# 临时变量用于计算
fwd_packet_lengths = []
bwd_packet_lengths = []
fwd_inter_arrival_times = []
bwd_inter_arrival_times = []
prev_fwd_packet_time = None
prev_bwd_packet_time = None


def packet_callback(packet):
    global prev_fwd_packet_time, prev_bwd_packet_time

    if IP in packet:
        packet_size = len(packet)
        metrics['Flow Bytes/s'] += packet_size
        metrics['Flow Packets/s'] += 1

        if packet[IP].src == 'your_client_ip':  # 替换为客户端IP地址
            metrics['Total Fwd Packets'] += 1
            fwd_packet_lengths.append(packet_size)

            if TCP in packet and packet[TCP].flags & 0x08:  # PSH flag
                metrics['Fwd PSH Flags'] += 1
            if TCP in packet and packet[TCP].flags & 0x20:  # URG flag
                metrics['Fwd URG Flags'] += 1

            if prev_fwd_packet_time is not None:
                iat = packet.time - prev_fwd_packet_time
                fwd_inter_arrival_times.append(iat)
            prev_fwd_packet_time = packet.time

        else:
            metrics['Total Backward Packets'] += 1
            bwd_packet_lengths.append(packet_size)

            if TCP in packet and packet[TCP].flags & 0x08:  # PSH flag
                metrics['Bwd PSH Flags'] += 1
            if TCP in packet and packet[TCP].flags & 0x20:  # URG flag
                metrics['Bwd URG Flags'] += 1

            if prev_bwd_packet_time is not None:
                iat = packet.time - prev_bwd_packet_time
                bwd_inter_arrival_times.append(iat)
            prev_bwd_packet_time = packet.time

        if TCP in packet:
            if packet[TCP].flags & 0x01:  # FIN flag
                metrics['FIN Flag Count'] += 1
            if packet[TCP].flags & 0x02:  # SYN flag
                metrics['SYN Flag Count'] += 1
            if packet[TCP].flags & 0x04:  # RST flag
                metrics['RST Flag Count'] += 1
            if packet[TCP].flags & 0x08:  # PSH flag
                metrics['PSH Flag Count'] += 1
            if packet[TCP].flags & 0x10:  # ACK flag
                metrics['ACK Flag Count'] += 1
            if packet[TCP].flags & 0x20:  # URG flag
                metrics['URG Flag Count'] += 1
            if packet[TCP].flags & 0x40:  # ECE flag
                metrics['ECE Flag Count'] += 1
            if packet[TCP].flags & 0x80:  # CWR flag
                metrics['CWE Flag Count'] += 1


def get_system_metrics():
    system_metrics = {
        'cpu_usage': psutil.cpu_percent(interval=1),
        'mem_usage': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
        'process_info': []
    }

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        system_metrics['process_info'].append(proc.info)

    return system_metrics


def reset_metrics():
    global fwd_packet_lengths, bwd_packet_lengths, fwd_inter_arrival_times, bwd_inter_arrival_times
    metrics['Flow Duration'] = 0
    metrics['Total Fwd Packets'] = 0
    metrics['Total Backward Packets'] = 0
    metrics['Fwd Packet Length Mean'] = 0
    metrics['Bwd Packet Length Mean'] = 0
    metrics['Flow Bytes/s'] = 0
    metrics['Flow Packets/s'] = 0
    metrics['Fwd IAT Mean'] = 0
    metrics['Bwd IAT Mean'] = 0
    metrics['Fwd PSH Flags'] = 0
    metrics['Bwd PSH Flags'] = 0
    metrics['Fwd URG Flags'] = 0
    metrics['Bwd URG Flags'] = 0
    metrics['Fwd Header Length'] = 0
    metrics['Bwd Header Length'] = 0
    metrics['Fwd Packets/s'] = 0
    metrics['Bwd Packets/s'] = 0
    metrics['Packet Length Std'] = 0
    metrics['Packet Length Variance'] = 0
    metrics['FIN Flag Count'] = 0
    metrics['SYN Flag Count'] = 0
    metrics['RST Flag Count'] = 0
    metrics['PSH Flag Count'] = 0
    metrics['ACK Flag Count'] = 0
    metrics['URG Flag Count'] = 0
    metrics['CWE Flag Count'] = 0
    metrics['ECE Flag Count'] = 0
    metrics['Down/Up Ratio'] = 0
    metrics['Average Packet Size'] = 0
    metrics['Fwd Segment Size Avg'] = 0
    metrics['Bwd Segment Size Avg'] = 0
    metrics['FWD Init Win Bytes'] = 0
    metrics['Bwd Init Win Bytes'] = 0
    metrics['Fwd Act Data Pkts'] = 0
    fwd_packet_lengths = []
    bwd_packet_lengths = []
    fwd_inter_arrival_times = []
    bwd_inter_arrival_times = []
    prev_fwd_packet_time = None
    prev_bwd_packet_time = None


def main():
    def calculate_and_print_metrics():
        while True:
            # 获取系统性能指标
            system_metrics = get_system_metrics()

            # 计算前向和反向数据包长度平均值
            if fwd_packet_lengths:
                metrics['Fwd Packet Length Mean'] = sum(fwd_packet_lengths) / len(fwd_packet_lengths)
            if bwd_packet_lengths:
                metrics['Bwd Packet Length Mean'] = sum(bwd_packet_lengths) / len(bwd_packet_lengths)

            # 计算前向和反向到达时间间隔平均值
            if fwd_inter_arrival_times:
                metrics['Fwd IAT Mean'] = sum(fwd_inter_arrival_times) / len(fwd_inter_arrival_times)
            if bwd_inter_arrival_times:
                metrics['Bwd IAT Mean'] = sum(bwd_inter_arrival_times) / len(bwd_inter_arrival_times)

            # 打印系统性能指标和网络流量特征
            combined_metrics = {**system_metrics, **metrics}
            print(json.dumps(combined_metrics, indent=4))
            exit()
            # 重置流量特征
            reset_metrics()

            # 等待一段时间
            time.sleep(1)

    threading.Thread(target=calculate_and_print_metrics).start()

    # 开始捕获数据包
    sniff(prn=packet_callback, store=0)


if __name__ == '__main__':
    main()
