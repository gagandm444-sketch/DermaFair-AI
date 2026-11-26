@echo off
title DermaFair AI - Healthcare Web Server
echo ================================================================
echo   DermaFair AI: Explainable Dermatology & Skin Tone Fairness
echo ================================================================
echo Starting backend server on http://127.0.0.1:5000/ ...
echo Opening your default browser...
start http://127.0.0.1:5000/
python backend_server.py 5000
pause
