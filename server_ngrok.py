from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pyngrok import ngrok
import asyncio

app = FastAPI()

# Mount folder static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Prosty chat w pamięci
clients = {}

@app.get("/")
async def get():
    with open("static/index.html") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    clients[username] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            for user, conn in clients.items():
                if conn != websocket:
                    await conn.send_text(f"{username}: {data}")
    except WebSocketDisconnect:
        del clients[username]

if __name__ == "__main__":
    import uvicorn

    # Uruchamiamy tunel ngrok
    public_url = ngrok.connect(8000)
    print("Twój publiczny URL:", public_url)

    # Start serwera FastAPI
    uvicorn.run(app, host="127.0.0.1", port=8000)
