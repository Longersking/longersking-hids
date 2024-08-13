from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, Depends
from typing import List, Optional
import json
from app.common import dealWsData
from pydantic import BaseModel
from app.models.base import SessionLocal
from app.models.ip_disabled import IpDisabled
from app.controllers.user_controller import get_current_user
from app.models.user import User


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[dict] = []

    async def connect(self, websocket: WebSocket, client_type: str, ip: Optional[str] = None):
        await websocket.accept()
        connection = {"websocket": websocket, "client_type": client_type, "ip": ip}
        self.active_connections.append(connection)
        print(f"Client connected: {websocket.client} with type: {client_type}, IP: {ip}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections = [conn for conn in self.active_connections if conn["websocket"] != websocket]
        print(f"Client disconnected: {websocket.client}")

    async def send_to_web(self, message: str, ip: Optional[str] = None):
        for connection in self.active_connections:
            # print(connection["client_type"] == "web",ip is None or connection["ip"] == ip)
            if connection["client_type"] == "web" and (connection["ip"] is None or connection["ip"] == ip):
                try:
                    await connection["websocket"].send_text(message)
                    # print(f"Message sent to {connection['websocket'].client}: {message}")
                except WebSocketDisconnect:
                    print("WebSocket disconnected")
                    self.disconnect(connection["websocket"])
                except Exception as e:
                    print(f"Error sending message: {e}")
                    self.disconnect(connection["websocket"])

    async def send_to_client(self, message: str, client_ip: Optional[str] = None):
        """
        向指定IP的客户端发送消息。如果没有指定IP，则发送给所有客户端。

        :param message: 要发送的消息内容。
        :param client_ip: 要发送的客户端的IP地址。如果为None，则发送给所有客户端。
        """
        for connection in self.active_connections:
            if connection["client_type"] == "client" and (client_ip is None or connection["ip"] == client_ip):
                try:
                    await connection["websocket"].send_text(message)
                    print(f"Message sent to {connection['ip']}: {message}")
                except WebSocketDisconnect:
                    print("WebSocket disconnected")
                    self.disconnect(connection["websocket"])
                except Exception as e:
                    print(f"Error sending message: {e}")
                    self.disconnect(connection["websocket"])

manager = ConnectionManager()
websocket_router = APIRouter()

@websocket_router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    client_type: str = Query(...),
    ip: Optional[str] = Query(None)
):
    await manager.connect(websocket, client_type, ip)
    try:
        while True:
            data = await websocket.receive_text()
            await handle_websocket(websocket, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"Error: {e}")
        manager.disconnect(websocket)

async def handle_websocket(websocket: WebSocket, data: str):
    try:
        data_json = json.loads(data)
        if "data" in data_json:
            # 调用 dealWsData 处理接收到的数据
            dealWsData(data_json)
            # 只发送到前端类型为 web 的客户端，如果指定了 IP 则只发给指定 IP 的客户端
            await manager.send_to_web(data, ip=data_json.get("ip"))
        else:
            print("No 'data' in received message.")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"Error: {e}")
        manager.disconnect(websocket)


# 定义API请求体的模型
class IPBlockRequest(BaseModel):
    ip_address: str  # 要封禁的IP地址
    client_ip: str  # 目标客户端的IP地址
    operator_id : str|int = None

@websocket_router.post("/block_ip")
async def block_ip(request: IPBlockRequest):
    """
    向指定的客户端发送封禁IP指令。

    :param request: 包含要封禁的IP地址和目标客户端IP地址的请求体。
    :return: 操作结果信息。
    """
    message = {"action": "blockIP", "data": request.ip_address}

    try:
        # 通过WebSocket管理器发送消息
        await manager.send_to_client(json.dumps(message), client_ip=request.client_ip)
        db = SessionLocal()
        # 将封禁IP记录到数据库
        ip_record = IpDisabled(host_ip=request.client_ip,ip=request.ip_address, operator=int(request.operator_id))

        db.add(ip_record)
        db.commit()

        return {"status": "success",
                "message": f"IP {request.ip_address} has been blocked on client {request.client_ip}"}
    except Exception as e:
        raise print(f"error : {e}")


@websocket_router.post("/unblock_ip")
async def unblock_ip(request: IPBlockRequest):
    """
    向指定的客户端发送解封IP指令。

    :param request: 包含要解封的IP地址和目标客户端IP地址的请求体。
    :return: 操作结果信息。
    """
    message = {"action": "unblockIP", "data": request.ip_address}

    try:
        # 通过WebSocket管理器发送消息
        await manager.send_to_client(json.dumps(message), client_ip=request.client_ip)

        # 连接数据库并删除对应的封禁记录
        db = SessionLocal()

        # 查找是否有对应的封禁记录
        ip_record = db.query(IpDisabled).filter_by(ip=request.ip_address, host_ip=request.client_ip).first()

        if ip_record:
            db.delete(ip_record)
            db.commit()

            return {"status": "success",
                    "message": f"IP {request.ip_address} has been unblocked on client {request.client_ip}"}
        else:
            return {"status": "failed", "message": "No matching record found to unblock."}
    except Exception as e:
        raise print(f"error : {e}")
