import os
import asyncio
from faster_whisper import WhisperModel
from app.core.config import MODEL_SIZE, DEVICE, COMPUTE_TYPE, MAX_GPU_PROCESSES
from app.services.notifier import notify
from app.services.translator import safe_translate

# Langsung load ke RTX 5090 pas server nyala!
print(f"🚀 Loading Whisper '{MODEL_SIZE}' on {DEVICE.upper()} with {COMPUTE_TYPE}...")
model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)
gpu_semaphore = asyncio.Semaphore(MAX_GPU_PROCESSES)

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
            await notify(job_id, {"status": "transcribing"})
            segments, info = await asyncio.to_thread(
                model.transcribe, filepath, language=input_lang if input_lang else None, beam_size=5
            )
        
        original_text = "".join([segment.text for segment in segments]).strip()
        detected_lang = info.language

        await notify(job_id, {"status": "translating"})
        translated_text = ""
        if original_text:
            translated_text = await asyncio.to_thread(
                safe_translate, original_text, input_lang, output_lang
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