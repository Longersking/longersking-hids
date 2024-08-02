import json
import websockets
import asyncio
import requests
import time

SERVER_URL = "ws://121.43.138.234:8003/ws"


async def send_data_to_server(url, ip, data, max_retries=5, retry_interval=2):
    retry_count = 0

    while retry_count < max_retries:
        try:
            async with websockets.connect(url) as websocket:
                message = json.dumps({
                    "ip": ip,
                    "data": data,
                    "type": "traffic_stats",
                    "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                })
                await websocket.send(message)
                print("数据发送成功")
                return  # 如果发送成功，函数将结束
        except (websockets.ConnectionClosed, websockets.InvalidURI, websockets.InvalidHandshake,
                websockets.WebSocketException) as e:
            print(f"连接失败: {e}")
            retry_count += 1
            if retry_count < max_retries:
                print(f"{retry_interval}秒后重试第{retry_count}次...")
                await asyncio.sleep(retry_interval)
            else:
                print(f"超过最大重试次数 {max_retries}，发送数据失败")
                return


def get_ip_address():
    try:
        response = requests.get("http://ipinfo.io/ip")
        ip = response.text.strip()
    except requests.RequestException:
        ip = '127.0.0.1'
    return ip
