from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import redis.asyncio as redis
import asyncio
import json

router = APIRouter()

# Konek ke Redis lokal lu (Port 6379)
redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

# Warna-warni Terminal biar gampang mantau log
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

@router.websocket("/ws/status/{job_id}")
async def websocket_status(ws: WebSocket, job_id: str):
    await ws.accept()
    print(f"{CYAN}🔗 [WS] HP Agen Terhubung untuk Job: {job_id}{RESET}")
    
    # Bikin pubsub object khusus untuk koneksi HP ini
    pubsub = redis_client.pubsub()
    channel_name = f"job_status:{job_id}"
    await pubsub.subscribe(channel_name)
    
    print(f"{CYAN}📡 [REDIS] Subscribed ke channel: {channel_name}{RESET}")
    
    try:
        while True:
            # Polling message dari Redis (Cek tiap 0.1 detik)
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=0.1)
            
            if message is not None:
                data_str = message['data']
                print(f"{GREEN}📨 [WS -> HP] Ngirim notif ke {job_id}: {data_str}{RESET}")
                
                await ws.send_text(data_str)
                
                # Parse JSON buat ngecek apakah AI udah kelar atau nge-bug
                try:
                    data_dict = json.loads(data_str)
                    if data_dict.get("status") in ["done", "error"]:
                        print(f"{YELLOW}🏁 [WS] Job {job_id} Selesai/Error. Menutup koneksi.{RESET}")
                        break # Keluar dari loop abadi
                except Exception as e:
                    print(f"{RED}❌ [WS] Gagal parse JSON dari Redis: {e}{RESET}")
            
            # Kasih nafas ke CPU biar nggak mentok 100%
            await asyncio.sleep(0.1)
            
    except WebSocketDisconnect:
        # HP agen tiba-tiba matiin aplikasi / hilang sinyal
        print(f"{YELLOW}🔌 [WS] HP Agen (Job {job_id}) terputus di tengah jalan.{RESET}")
    except Exception as e:
        print(f"{RED}❌ [WS] Error sistem di Job {job_id}: {e}{RESET}")
    finally:
        # BERSIH-BERSIH (PENTING BANGET BIAR RAM NGGAK BOCOR)
        print(f"{CYAN}🧹 [WS] Bersih-bersih Job {job_id}... Unsubscribe Redis.{RESET}")
        await pubsub.unsubscribe(channel_name)
        try:
            await ws.close()
        except Exception:
            pass # Cuekin aja kalau websocket-nya udah keburu ditutup duluan sama HP
        print(f"{CYAN}✅ [WS] Job {job_id} Session Closed.{RESET}\n")