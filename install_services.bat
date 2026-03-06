@echo off
echo ==========================================
echo INSTALLING VTT PRODUCTION SERVICES
echo ==========================================

:: Sesuaikan path uvicorn lu. 
:: Berdasarkan log lu sebelumnya, lu pakai Python global di C:\Program Files\Python312
SET UVICORN_PATH="C:\Python312\Scripts\uvicorn.exe"
SET APP_DIR="C:\voice-to-text"

:: Buat folder logs kalau belum ada
if not exist "%APP_DIR%\logs" mkdir "%APP_DIR%\logs"

echo [1/3] Setup Worker 4051...
nssm install VTT_Worker_4051 %UVICORN_PATH% app.main:app --host 127.0.0.1 --port 4051
nssm set VTT_Worker_4051 AppDirectory %APP_DIR%
nssm set VTT_Worker_4051 AppStdout "%APP_DIR%\logs\worker_4051.log"
nssm set VTT_Worker_4051 AppStderr "%APP_DIR%\logs\worker_4051_error.log"

echo [2/3] Setup Worker 4052...
nssm install VTT_Worker_4052 %UVICORN_PATH% app.main:app --host 127.0.0.1 --port 4052
nssm set VTT_Worker_4052 AppDirectory %APP_DIR%
nssm set VTT_Worker_4052 AppStdout "%APP_DIR%\logs\worker_4052.log"
nssm set VTT_Worker_4052 AppStderr "%APP_DIR%\logs\worker_4052_error.log"

echo [3/3] Setup Worker 4053...
nssm install VTT_Worker_4053 %UVICORN_PATH% app.main:app --host 127.0.0.1 --port 4053
nssm set VTT_Worker_4053 AppDirectory %APP_DIR%
nssm set VTT_Worker_4053 AppStdout "%APP_DIR%\logs\worker_4053.log"
nssm set VTT_Worker_4053 AppStderr "%APP_DIR%\logs\worker_4053_error.log"

echo.
echo Menyalakan semua service...
nssm start VTT_Worker_4051
nssm start VTT_Worker_4052
nssm start VTT_Worker_4053

echo.
echo ✅ Beres Bro! 3 Worker udah jalan di background.
pause