REM Activate the virtual environment
call "venv\Scripts\activate"

REM Check if activation was successful
if %errorlevel% neq 0 (
    echo Failed to activate virtual environment.
	pause
)

REM Open the URL in the default browser
start http://127.0.0.1:8000/

REM Run the Django development server
python manage.py runserver

pause