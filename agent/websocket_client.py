import json
import websocket

class WebSocketClient:
    def __init__(self, uri: str):
        self.uri = uri
        self.ws = None

    def connect(self):
        self.ws = websocket.create_connection(self.uri)

    def send_message(self, message: str):
        if self.ws is not None:
            self.ws.send(json.dumps(message))

    def close(self):
        if self.ws is not None:
            self.ws.close()
