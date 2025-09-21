@echo off
echo 🚀 YTGraphX Deployment Helper
echo ================================
echo.

echo Choose deployment option:
echo 1. Streamlit Cloud (Recommended)
echo 2. Local Network Sharing
echo 3. Docker
echo 4. Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto streamlit_cloud
if "%choice%"=="2" goto local_network
if "%choice%"=="3" goto docker
if "%choice%"=="4" goto exit
goto invalid

:streamlit_cloud
echo.
echo 📋 Streamlit Cloud Deployment Steps:
echo 1. Push your code to GitHub
echo 2. Go to https://share.streamlit.io
echo 3. Sign in with GitHub
echo 4. Click "New app"
echo 5. Select your repository
echo 6. Main file: streamlit_app.py
echo 7. Add API key in secrets
echo.
echo Your app will be available at: https://YOUR_USERNAME-ytgraphx.streamlit.app
goto end

:local_network
echo.
echo 🌐 Starting local network server...
echo Your app will be available at: http://YOUR_IP:8501
echo.
streamlit run streamlit_app.py --server.address 0.0.0.0
goto end

:docker
echo.
echo 🐳 Building Docker container...
docker build -t ytgraphx .
echo.
echo 🚀 Starting Docker container...
docker run -p 8501:8501 ytgraphx
goto end

:invalid
echo Invalid choice. Please try again.
goto end

:exit
echo Goodbye!
goto end

:end
pause
