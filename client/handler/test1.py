import subprocess
import dpkt
import socket

def start_tcpdump(interface):
    # 启动 tcpdump 命令进行抓包，并将输出重定向到管道
    return subprocess.Popen(
        ['sudo', 'tcpdump', '-i', interface, '-w', '-', 'tcp', 'port', '8003'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

def process_packet(packet, packet_cache):
    eth = dpkt.ethernet.Ethernet(packet)
    ip = eth.data
    tcp = ip.data

    # 检查是否为 TCP 数据包并且包含数据
    if not isinstance(tcp, dpkt.tcp.TCP) or len(tcp.data) == 0:
        return

    # 检查是否为 HTTP 数据包
    if tcp.dport == 8003 or tcp.sport == 8003:
        stream_id = (socket.inet_ntoa(ip.src), tcp.sport, socket.inet_ntoa(ip.dst), tcp.dport)
        if stream_id not in packet_cache:
            packet_cache[stream_id] = b""
        packet_cache[stream_id] += tcp.data

        # 尝试解析 HTTP 请求
        try:
            if len(packet_cache[stream_id]) > 10 * 1024:  # 设置一个缓存上限，避免缓存过大
                print(f"Stream {stream_id} data is too large, skipping")
                packet_cache[stream_id] = b""
                return

            http_request = dpkt.http.Request(packet_cache[stream_id])
            print(f"HTTP Request from {socket.inet_ntoa(ip.src)} to {socket.inet_ntoa(ip.dst)}")
            print(f"Method: {http_request.method}")
            print(f"Host: {http_request.headers.get('host', '')}")
            print(f"Path: {http_request.uri}")
            print("Headers:")
            for header, value in http_request.headers.items():
                print(f"  {header}: {value}")
            if http_request.body:
                print(f"Payload: {http_request.body.decode('utf-8', errors='ignore')}")
            print("\n")
            # 清理缓存
            packet_cache[stream_id] = b""
        except dpkt.NeedData as e:
            pass
            # print(f"Need more data to parse HTTP request: {e}")
        except dpkt.UnpackError as e:
            pass
            # print(f"Failed to unpack HTTP request: {e}")
            # 出现解析错误，清理缓存以避免下次错误
            packet_cache[stream_id] = b""
        except Exception as e:
            pass
            # print(f"Unexpected error: {e}")
            # print(f"Raw stream data: {packet_cache[stream_id]}")
            # 出现意外错误，清理缓存以避免下次错误
            packet_cache[stream_id] = b""

def capture_packets(tcpdump_proc):
    packet_cache = {}
    pcap_reader = dpkt.pcap.Reader(tcpdump_proc.stdout)
    for timestamp, packet in pcap_reader:
        process_packet(packet, packet_cache)

if __name__ == "__main__":
    interface = 'eth0'  # 替换为你的网络接口

    # 启动 tcpdump 进程
    tcpdump_proc = start_tcpdump(interface)

    try:
        # 捕获和处理数据包
        capture_packets(tcpdump_proc)
    except KeyboardInterrupt:
        print("捕获已终止")
    finally:
        tcpdump_proc.terminate()
