@echo off
echo 🚀 PyTerm Heroku Deployment Script
echo.

REM Check if Heroku CLI is installed
heroku --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Heroku CLI is not installed.
    echo Please install it from: https://devcenter.heroku.com/articles/heroku-cli
    echo Then restart this script.
    pause
    exit /b 1
)

echo ✅ Heroku CLI found

REM Login to Heroku
echo 🔑 Logging into Heroku (browser will open)...
heroku login

REM Prompt for app name
set /p APP_NAME="Enter your app name (e.g., kushal-pyterm-demo): "

REM Create Heroku app
echo 📦 Creating Heroku app: %APP_NAME%
heroku create %APP_NAME%

REM Deploy to Heroku
echo 🚀 Deploying to Heroku...
git push heroku main

REM Open the app
echo 🌐 Opening your live app...
heroku open

echo.
echo ✅ Deployment complete!
echo Your app is live at: https://%APP_NAME%.herokuapp.com
echo.
echo 📊 Useful commands:
echo   heroku logs --tail    (view logs)
echo   heroku restart        (restart app)
echo   heroku open          (open app)
echo.
pause
