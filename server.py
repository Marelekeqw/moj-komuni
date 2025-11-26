from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
import base64

app = FastAPI()
from fastapi.responses import RedirectResponse

@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")
                            
app.mount("/static", StaticFiles(directory="static"), name="static")

clients = {}

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    clients[username] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            import json
            obj = json.loads(data)
            if "message" in obj:
                for user, conn in clients.items():
                    await conn.send_text(f"{username}: {obj['message']}")
            if "file" in obj:
                filename = obj["file"]
                content = base64.b64decode(obj["data"].split(",")[1])
                path = os.path.join("uploads", filename)
                with open(path, "wb") as f:
                    f.write(content)
                for user, conn in clients.items():
                    await conn.send_text(f"{username} wysłał plik: {filename}")
    except:
        del clients[username]
