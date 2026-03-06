import shutil
import os
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks
from app.services.ai_worker import process_file

router = APIRouter()

# Bikin folder otomatis kalau belum ada
if not os.path.exists("temp_audio"):
    os.makedirs("temp_audio")

@router.post("/upload")
async def upload_file(
    background_tasks: BackgroundTasks,
    input_lang: str = Form(""), 
    output_lang: str = Form("id"),
    file: UploadFile = File(...),
    job_id: str = Form(...)
):
    temp_path = f"temp_audio/temp_{job_id}_{file.filename}"
    
    # BACA STREAMING: Langsung tulis ke disk, nggak makan RAM
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Lempar ke background task buat di proses
    background_tasks.add_task(process_file, temp_path, job_id, input_lang, output_lang)

    return {"status": "accepted", "filename": file.filename, "job_id": job_id}