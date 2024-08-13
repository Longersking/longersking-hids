import pcapy
from impacket.ImpactDecoder import EthDecoder
from impacket.ImpactPacket import TCP, IP, UDP, ICMP

class PacketSniffer:
    def __init__(self, interface):
        self.interface = interface
        self.decoder = EthDecoder()
        self.pcap = pcapy.open_live(interface, 65536, 1, 0)
        self.tcp_streams = {}

    def start(self):
        print(f"Starting packet capture on interface {self.interface}")
        self.pcap.loop(0, self.packet_callback)

    def packet_callback(self, header, packet):
        eth_packet = self.decoder.decode(packet)
        packet_info = {
            "src_ip": None,
            "src_port": None,
            "dst_ip": None,
            "dst_port": None,
            "protocol": None,
            "size": len(packet),
            "content": None
        }

        if isinstance(eth_packet.child(), IP):
            ip_packet = eth_packet.child()
            packet_info["src_ip"] = ip_packet.get_ip_src()
            packet_info["dst_ip"] = ip_packet.get_ip_dst()

            if isinstance(ip_packet.child(), TCP):
                tcp_packet = ip_packet.child()
                packet_info["src_port"] = tcp_packet.get_th_sport()
                packet_info["dst_port"] = tcp_packet.get_th_dport()
                packet_info["protocol"] = "TCP"

                stream_id = (packet_info["src_ip"], packet_info["src_port"], packet_info["dst_ip"], packet_info["dst_port"])
                if stream_id not in self.tcp_streams:
                    self.tcp_streams[stream_id] = b""

                self.tcp_streams[stream_id] += tcp_packet.get_data_as_string()

                if tcp_packet.get_th_dport() == 8003 or tcp_packet.get_th_sport() == 8003:
                    packet_info["protocol"] = "HTTP"
                    packet_info["content"] = self.parse_http_stream(self.tcp_streams[stream_id])
                    if packet_info["content"] is not None:
                        # 已经完整解析，移除缓存的数据
                        print(f"Complete HTTP request captured: {packet_info['content']}")
                        self.tcp_streams[stream_id] = b""
                elif tcp_packet.get_th_dport() == 443 or tcp_packet.get_th_sport() == 443:
                    packet_info["protocol"] = "HTTPS"
                    packet_info["content"] = self.tcp_streams[stream_id].hex()
                    # print(packet_info)
                    self.tcp_streams[stream_id] = b""  # 对于 HTTPS 流，不进行进一步的解析，直接清空缓存
                # elif tcp_packet.get_th_dport() == 22 or tcp_packet.get_th_sport() == 22:
                #     packet_info["protocol"] = "SSH"
                #     packet_info["content"] = self.tcp_streams[stream_id].hex()
                #     self.tcp_streams[stream_id] = b""  # SSH 流的处理方式与 HTTPS 类似
                else:
                    packet_info["content"] = tcp_packet.get_data_as_string()

            elif isinstance(ip_packet.child(), UDP):
                udp_packet = ip_packet.child()
                packet_info["src_port"] = udp_packet.get_uh_sport()
                packet_info["dst_port"] = udp_packet.get_uh_dport()
                packet_info["protocol"] = "UDP"
                packet_info["content"] = udp_packet.get_data_as_string()

            elif isinstance(ip_packet.child(), ICMP):
                icmp_packet = ip_packet.child()
                packet_info["protocol"] = "ICMP"
                packet_info["content"] = icmp_packet.get_data_as_string()


    def parse_http_stream(self, data):
        try:
            # 尝试分割头和体
            headers, body = data.split(b'\r\n\r\n', 1)
            headers = headers.decode('utf-8', errors='ignore')

            # 分割请求行
            request_line, *header_lines = headers.split('\r\n')
            try:
                method, url, version = request_line.split(' ', 2)
            except ValueError as e:
                print(f"Error parsing request line: {e}")
                return None  # 解析失败，返回 None 继续缓存

            headers_dict = {}
            content_length = 0
            for line in header_lines:
                # 处理可能没有冒号或其他格式异常的请求头
                if ': ' in line:
                    key, value = line.split(': ', 1)
                    headers_dict[key] = value
                    if key.lower() == "content-length":
                        content_length = int(value)
                else:
                    print(f"Skipping invalid header line: {line}")

            # 检查接收到的body是否与Content-Length相匹配
            if len(body) < content_length:
                print(f"Waiting for more data... Received {len(body)} bytes, expected {content_length} bytes.")
                return None  # 数据不完整，继续等待

            return {
                "method": method,
                "url": url,
                "version": version,
                "headers": headers_dict,
                "body": body.decode('utf-8', errors='ignore')
            }
        except (ValueError, UnicodeDecodeError) as e:
            # 如果解析失败，返回 None 继续缓存
            print(f"Error parsing HTTP stream: {e}")
            return None

if __name__ == "__main__":
    sniffer = PacketSniffer("eth0")
    sniffer.start()
