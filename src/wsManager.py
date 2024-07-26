"""
WebSocket接続を管理するクラス
"""

from typing import Dict, List
from fastapi import WebSocket


class WSManager:
    """
    WebSocket接続を管理するクラス
    """

    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, id, websocket: WebSocket):
        await websocket.accept()
        await websocket.send_text(f"[Connected] Your id is {id}")

        if id not in self.active_connections:
            self.active_connections[id] = []

        self.active_connections[id].append(websocket)

    async def disconnect(self, id, websocket: WebSocket):
        await websocket.close()
        self.active_connections[id].remove(websocket)

    async def send(self, id: int, message: bytes):
        if id not in self.active_connections:
            return

        for connection in self.active_connections[id]:
            try:
                await connection.send_bytes(message)
            except:
                self.active_connections[id].remove(connection)
