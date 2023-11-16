@echo off


rem Check if venv folder exists. If not creates one
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

rem Install dependencies
pip install -r requirements.txt

rem Activate the virtual environment
call venv\Scripts\activate

rem Run Flask in the background
start "Flask Web Server" /B venv\Scripts\python.exe web_story.py

rem Pause to allow Flask to start
timeout /t 2

rem Open the default web browser with the Flask app
start http://127.0.0.1:5000

rem Deactivate the virtual environment (optional)
call venv\Scripts\deactivate

pause
