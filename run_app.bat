@echo off
if not exist .venv\Scripts\activate (
    echo Virtual environment not found. Run setup_windows.bat first.
    exit /b 1
)
call .venv\Scripts\activate
python -m etg_scheduler
