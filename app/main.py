from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import upload
from app.api.websockets import status_ws

app = FastAPI(title="Voice-to-Text API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Daftarin rute API & Websocket
app.include_router(upload.router)
app.include_router(status_ws.router)

@app.get("/")
def read_root():
    return {"message": "VTT API is running!"}