import json
import websockets
import asyncio
import requests
import time
from queue import Empty, Queue

SERVER_URL = "ws://121.43.138.234:8003/ws"

async def send_data(websocket, ip, data, data_type="traffic_stats"):
    message = json.dumps({
        "ip": ip,
        "data": data,
        "type": data_type,
        "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    })
    await websocket.send(message)
    print(f"数据发送成功: {data_type}")

async def send_data_to_server(url, ip, **queues):
    ws_url = f"{url}?client_type=client&ip={ip}"  # 包含客户端类型和IP地址
    while True:
        try:
            async with websockets.connect(ws_url) as websocket:
                print(f"连接成功: {ip}")
                while True:
                    for name, queue in queues.items():
                        try:
                            current_stats = queue.get_nowait()  # 非阻塞地从队列获取数据
                            await send_data(websocket, ip, json.dumps(current_stats), name)
                            queue.task_done()  # 标记任务完成
                        except Empty:
                            continue
                    await asyncio.sleep(0.1)  # 稍微休眠，避免过多资源占用
        except (websockets.ConnectionClosed, websockets.InvalidURI, websockets.InvalidHandshake,
                websockets.WebSocketException) as e:
            print(f"连接失败: {e}")
            print("1秒后重试...")
            await asyncio.sleep(1)

def get_ip_address():
    try:
        response = requests.get("http://ipinfo.io/ip")
        ip = response.text.strip()
    except requests.RequestException:
        ip = '127.0.0.1'
    return ip

async def receive_commands(url, ip_blocker):
    ws_url = f"{url}?client_type=client&ip={get_ip_address()}"
    while True:
        try:
            async with websockets.connect(ws_url) as websocket:
                print("WebSocket connection established for command reception.")
                while True:
                    message = await websocket.recv()
                    print(f"Received command: {message}")
                    data = json.loads(message)
                    action = data.get("action")
                    if action == "blockIP":
                        ip_address = data.get("data")
                        ip_blocker.block_ip(ip_address)
                    elif action == "unblockIP":
                        ip_address = data.get("data")
                        ip_blocker.unblock_ip(ip_address)
                    # 可以在这里扩展更多指令的处理逻辑
        except (websockets.ConnectionClosed, websockets.InvalidURI, websockets.InvalidHandshake,
                websockets.WebSocketException) as e:
            print(f"WebSocket connection failed: {e}")
            print("Retrying connection in 1 second...")
            await asyncio.sleep(1)

if __name__ == "__main__":
    ip = get_ip_address()
    asyncio.run(send_data_to_server(SERVER_URL, ip, traffic_stats=Queue(), system_load=Queue()))
