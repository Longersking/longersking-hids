import asyncio
import websockets
import json
from .utils import SERVER_URL

async def send_data(stats, message_type):
    while True:
        try:
            async with websockets.connect(SERVER_URL) as websocket:
                if websocket.open:
                    await websocket.send(json.dumps({'type': message_type, 'data': stats}))
                else:
                    print("WebSocket is closed, cannot send data")
                break
        except Exception as e:
            print(f"Error sending data: {e}")
            await asyncio.sleep(1)  # 等待1秒后重试

async def send_packet_data(stats):
    await send_data(stats, "packet")
