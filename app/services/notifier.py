from fastapi import WebSocket
import json
import redis.asyncio as redis

# clients = {}
redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

# async def notify(job_id: str, message: dict):
#     if job_id not in clients:
#         return
#     dead_clients = []
#     for ws in clients[job_id]:
#         try:
#             await ws.send_text(json.dumps(message))
#         except Exception:
#             dead_clients.append(ws)
#     for dc in dead_clients:
#         clients[job_id].remove(dc)

async def notify(job_id: str, message: dict):
    channel_name = f"job_status:{job_id}"
    
    # Ubah dict ke JSON string sebelum dilempar ke Redis
    payload = json.dumps(message)
    
    # Teriak ke seantero server!
    await redis_client.publish(channel_name, payload)
    print(f"📢 [REDIS] Published to {channel_name}: {message['status']}")