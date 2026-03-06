@echo off
if not exist "temp_audio" mkdir temp_audio
echo Menjalankan VTT API di Port 4051...
uvicorn app.main:app --host 127.0.0.1 --port 4051 --reload
pause