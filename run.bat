@echo off
echo ====================================================================
echo Starting DermaFair AI - Healthcare Deep Learning Web Platform
echo ====================================================================
echo Checking Python environment...

python -c "import flask" >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Flask detected. Launching full Flask production server...
    python app.py
) else (
    echo [INFO] Launching standalone development server on port 5000...
    echo [TIP] Run 'pip install -r requirements.txt' to install full dependencies.
    python run_standalone.py 5000
)

pause
