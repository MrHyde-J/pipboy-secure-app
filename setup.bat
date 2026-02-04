@echo off
echo Setting up Vault-Tec Secure Web Application...
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Failed to create virtual environment
    pause
    exit /b 1
)

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip

echo Step 4: Installing requirements...
pip install Flask==3.0.0 Flask-SQLAlchemy==3.0.5 Flask-Login==0.6.2 Werkzeug==3.0.1 bleach==6.0.0

echo.
echo Installation complete!
echo.
echo To run the application:
echo 1. Activate virtual environment: venv\Scripts\activate
echo 2. Run: python app.py
echo 3. Open browser to: http://localhost:5000
echo.
pause