class PacketAnalyzer:
    def __init__(self):
        self.protocol_sizes = {
            'TCP': 0,
            'UDP': 0,
            'HTTP': 0,
            'HTTPS': 0,
            'SSH': 0,
            'DNS': 0,
            'ICMP': 0,
            'IP': 0  # 添加 IP 协议
        }

    def analyze_packets(self, packets):
        for packet in packets:
            packet_size = packet['size']
            if packet['proto'] == 'TCP':
                self.protocol_sizes['TCP'] += packet_size
            elif packet['proto'] == 'UDP':
                self.protocol_sizes['UDP'] += packet_size
            elif packet['proto'] == 'ICMP':
                self.protocol_sizes['ICMP'] += packet_size
            elif packet['proto'] == 'IP':
                self.protocol_sizes['IP'] += packet_size
        return self.protocol_sizes
