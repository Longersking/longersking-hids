from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import List
import json
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.traffic_data import TrafficData
from datetime import datetime
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"Client connected: {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"Client disconnected: {websocket.client}")

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                self.disconnect(connection)
            except Exception as e:
                print(f"Error sending message: {e}")

manager = ConnectionManager()
websocket_router = APIRouter()

async def handle_websocket(websocket: WebSocket, db: Session):
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received data: {data}")
            data_json = json.loads(data)
            if "data" in data_json:
                try:
                    traffic_data = json.loads(data_json["data"])
                    ip = data_json.get("ip", "")
                    total_sent = traffic_data.get("total_sent", 0)
                    total_received = traffic_data.get("total_received", 0)
                    protocol_sizes = traffic_data.get("protocol_sizes", {})
                    timestamp = datetime.strptime(data_json.get("time", ""), "%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    print(f"Error sending data: {e}")
                new_traffic_data = TrafficData(
                    ip=ip,
                    total_sent=total_sent,
                    total_received=total_received,
                    protocol_sizes=protocol_sizes,
                    timestamp=timestamp
                )
                db.add(new_traffic_data)
                db.commit()

                await manager.broadcast(data)
            else:
                print("No 'data' in received message.")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"Error: {e}")
        manager.disconnect(websocket)

@websocket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await manager.connect(websocket)
    await handle_websocket(websocket, db)
