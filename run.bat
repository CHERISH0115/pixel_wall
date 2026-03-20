@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 启动 Pixel Wall...
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)
python main.py
pause
