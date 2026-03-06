from fastapi import WebSocket
import json

clients = {}

async def notify(job_id: str, message: dict):
    if job_id not in clients:
        return
    dead_clients = []
    for ws in clients[job_id]:
        try:
            await ws.send_text(json.dumps(message))
        except Exception:
            dead_clients.append(ws)
    for dc in dead_clients:
        clients[job_id].remove(dc)