from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.notifier import clients

router = APIRouter()

@router.websocket("/ws/status/{job_id}")
async def websocket_status(ws: WebSocket, job_id: str):
    await ws.accept()
    if job_id not in clients:
        clients[job_id] = set()
    clients[job_id].add(ws)
    try:
        while True:
            await ws.receive_text()  # keep alive
    except WebSocketDisconnect:
        clients[job_id].remove(ws)
        if not clients[job_id]:
            del clients[job_id]