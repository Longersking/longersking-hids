from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

from utils.host_handler.sys_monitor import Monitor
from .. import common

# 配置路由
test_router = APIRouter()

# WebSocket 连接管理
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@test_router.websocket("/load_info")
async def cpu_message(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            cpu_info = await websocket.receive_text()  # 等待客户端的请求信息
            print(cpu_info)
            await manager.send_personal_message(common.dataReturn(1, msg="system message", data=cpu_info), websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


