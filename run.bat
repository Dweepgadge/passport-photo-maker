@echo off
echo ========================================================
echo   Starting AI Official ID & Passport Photo Maker
echo ========================================================
echo.
cd /d "%~dp0"
echo Checking dependencies...
python -m pip install -r requirements.txt
echo.
echo Launching server at http://localhost:8000 ...
echo Open your browser to http://localhost:8000
echo Press Ctrl+C in this terminal to stop the server.
echo.
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
pause
