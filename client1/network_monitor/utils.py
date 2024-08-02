import socket
import time

SERVER_URL = "ws://localhost:8003/ws"
PACKET_LOSS_INTERVAL = 10  # 丢包率计算间隔，单位秒
SIMULATED_PACKET_LOSS_RATE = 0.001  # 模拟的较小丢包率数值

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
        ip = '127.0.0.111'
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip
