import os
import asyncio
from faster_whisper import WhisperModel
from app.core.config import MODEL_SIZE, DEVICE, COMPUTE_TYPE, MAX_GPU_PROCESSES
from app.services.notifier import notify
from app.services.translator import safe_translate

gpu_semaphore = asyncio.Semaphore(MAX_GPU_PROCESSES)

BLUE = "\033[94m"
RESET = "\033[0m"

print(f"{BLUE}🚀 Loading Whisper '{MODEL_SIZE}' on {DEVICE.upper()} with VAD Filter...{RESET}")
model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)

async def send_heartbeat(job_id: str):
    try:
        while True:
            await asyncio.sleep(10)
            await notify(job_id, {"status": "processing", "message": "AI is working, please wait..."})
    except asyncio.CancelledError:
        pass

async def process_file(filepath: str, job_id: str, input_lang: str, output_lang: str):
    heartbeat_task = asyncio.create_task(send_heartbeat(job_id))
    
    try:
        await notify(job_id, {"status": "waiting_in_queue", "message": "Waiting for AI worker..."})
        
        # Masuk Gembok Antrean GPU
        async with gpu_semaphore:
            print(f"{BLUE}[{job_id}] Memulai transkripsi akurasi tinggi...{RESET}")
            await notify(job_id, {"status": "transcribing"})
           
            segments, info = await asyncio.to_thread(
                model.transcribe, 
                filepath, 
                language=input_lang if input_lang else None, 
                beam_size=5,
                vad_filter=True, 
                vad_parameters=dict(min_silence_duration_ms=500),
                condition_on_previous_text=False
            )
        
            original_text = "".join([segment.text for segment in segments]).strip()
            detected_lang = info.language

        await notify(job_id, {"status": "translating"})
        translated_text = ""
        if original_text:
            translated_text = await asyncio.to_thread(
                safe_translate, original_text, detected_lang, output_lang
            )

        await notify(job_id, {
            "status": "done",
            "original_text": original_text,
            "translated_text": translated_text,
            "detected_lang": detected_lang,
        })

    except Exception as e:
        await notify(job_id, {"status": "error", "message": str(e)})
    finally:
        heartbeat_task.cancel()
        if os.path.exists(filepath):
            os.remove(filepath)