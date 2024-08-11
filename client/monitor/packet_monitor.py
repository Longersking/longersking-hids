import json
import threading
import pcapy
from impacket.ImpactDecoder import EthDecoder
from impacket.ImpactPacket import TCP, IP, UDP, ICMP
from queue import Queue
from config import HTTP_Ports,HTTPS_Ports

class PacketMonitor:
    def __init__(self, interface, queue,matcher):
        self.interface = interface
        self.decoder = EthDecoder()
        self.pcap = pcapy.open_live(interface, 65536, 1, 0)
        self.tcp_streams = {}
        self.queue = queue
        self.matcher = matcher

    def start(self):
        print(f"Starting packet capture on interface {self.interface}")
        threading.Thread(target=self.capture_loop, daemon=True).start()

    def capture_loop(self):
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
            "content": None,
            "is_dangerous" : None,
            "matches" : None,
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

                stream_id = (
                    packet_info["src_ip"], packet_info["src_port"], packet_info["dst_ip"], packet_info["dst_port"]
                )
                if stream_id not in self.tcp_streams:
                    self.tcp_streams[stream_id] = b""

                self.tcp_streams[stream_id] += tcp_packet.get_data_as_string()

                if tcp_packet.get_th_dport() in HTTP_Ports or tcp_packet.get_th_sport() in HTTP_Ports:
                    packet_info["protocol"] = "HTTP"
                    http_content = self.parse_http_stream(self.tcp_streams[stream_id])
                    if http_content is not None:
                        packet_info["content"] = http_content
                        # 匹配字符串
                        res = self.matcher.match(json.dumps(http_content))
                        if res is not None and res != []:
                            packet_info["is_dangerous"] = 1
                            packet_info["matches"] = res
                            print(f"HTTP match: {res}")
                        self.tcp_streams[stream_id] = b""
                elif tcp_packet.get_th_dport()  in HTTPS_Ports or tcp_packet.get_th_sport() in HTTP_Ports:
                    packet_info["protocol"] = "HTTPS"
                    packet_info["content"] = self.tcp_streams[stream_id].hex()
                    self.tcp_streams[stream_id] = b""
                else:
                    packet_info["content"] = self.tcp_streams[stream_id].hex()
                    self.tcp_streams[stream_id] = b""

            elif isinstance(ip_packet.child(), UDP):
                udp_packet = ip_packet.child()
                packet_info["src_port"] = udp_packet.get_uh_sport()
                packet_info["dst_port"] = udp_packet.get_uh_dport()
                packet_info["protocol"] = "UDP"
                packet_info["content"] = udp_packet.get_data_as_string().hex()

            elif isinstance(ip_packet.child(), ICMP):
                icmp_packet = ip_packet.child()
                packet_info["protocol"] = "ICMP"
                packet_info["content"] = icmp_packet.get_data_as_string().hex()

            # 确保 content 不为空
            if packet_info['content'] and packet_info['content'] != "" and packet_info['protocol'] not in  ["TCP",'HTTPS']:
                # print(packet_info)
                print(f"捕获到{packet_info['protocol']}，已写入队列")
                self.queue.put(packet_info)

    def parse_http_stream(self, data):
        try:
            headers, body = data.split(b'\r\n\r\n', 1)
            headers = headers.decode('utf-8', errors='ignore')

            request_line, *header_lines = headers.split('\r\n')
            method, url, version = request_line.split(' ', 2)

            headers_dict = {}
            content_length = 0
            for line in header_lines:
                if ': ' in line:
                    key, value = line.split(': ', 1)
                    headers_dict[key] = value
                    if key.lower() == "content-length":
                        content_length = int(value)

            if len(body) < content_length:
                print(f"Waiting for more data... Received {len(body)} bytes, expected {content_length} bytes.")
                return None

            return {
                "method": method,
                "url": url,
                "version": version,
                "headers": headers_dict,
                "body": body.decode('utf-8', errors='ignore')
            }
        except (ValueError, UnicodeDecodeError) as e:
            return None

if __name__ == "__main__":
    queue = Queue()
    monitor = PacketMonitor("eth0", queue)
    monitor.start()

    while True:
        packet_info = queue.get()
        print(packet_info)
