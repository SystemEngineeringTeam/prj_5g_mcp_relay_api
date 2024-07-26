from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from src.wsManager import WSManager


app = FastAPI()
manager = WSManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.api_route("/", methods=["GET", "POST"])
async def read_root():
    return HTMLResponse("Hello World!")


@app.post("/api/raw/{id}")
async def post_raw_data(id: int, req: Request):
    """
    HTTP POST でデータを受け取り、WebSocket で接続しているクライアントにデータを送信する
    """

    data = await req.body()

    # データを WebSocket で接続しているクライアントに送信
    await manager.send(id, data)

    return data


@app.websocket("/ws/{id}")
async def websocket_endpoint(id: int, websocket: WebSocket):
    """
    WebSocket 接続を受け付けるエンドポイント
    """

    # WebSocket 接続を管理するクラスに登録
    await manager.connect(id, websocket)

    try:
        while True:
            # メッセージを受信
            data = await websocket.receive_text()
            await websocket.send_text(f"Received: {data}")

    except WebSocketDisconnect:
        # WebSocket 接続が切断された場合は解除
        await manager.disconnect(id, websocket)

@app.api_route("/*")
async def read_root():
    return HTMLResponse("File not found", status_code=404)
