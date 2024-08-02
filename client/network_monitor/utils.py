import socket
import time
import requests

SERVER_URL = "ws://121.43.138.234:8003/ws"
PACKET_LOSS_INTERVAL = 10  # 丢包率计算间隔，单位秒
SIMULATED_PACKET_LOSS_RATE = 0.001  # 模拟的较小丢包率数值

def get_ip_address():
    try:
        # 使用公共的IP查询服务来获取公网IP
        response = requests.get("http://ipinfo.io/ip")
        ip = response.text.strip()
    except requests.RequestException:
        ip = '127.0.0.1'
    return ip