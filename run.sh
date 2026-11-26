#!/usr/bin/env bash
echo "===================================================================="
echo "Starting DermaFair AI - Healthcare Deep Learning Web Platform"
echo "===================================================================="

if python3 -c "import flask" >/dev/null 2>&1; then
    echo "[INFO] Flask detected. Launching full Flask production server..."
    python3 app.py
else
    echo "[INFO] Launching standalone development server on port 5000..."
    echo "[TIP] Run 'pip3 install -r requirements.txt' to install full dependencies."
    python3 run_standalone.py 5000
fi
