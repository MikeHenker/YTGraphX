# 🚀 YTGraphX Deployment Guide

## Option 1: Streamlit Cloud (Easiest)

### Steps:
1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - YouTube Statistics Tracker"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YTGraphX.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository: `YOUR_USERNAME/YTGraphX`
   - Main file path: `streamlit_app.py`
   - Click "Deploy"

3. **Set Environment Variables:**
   - In Streamlit Cloud dashboard
   - Go to "Settings" → "Secrets"
   - Add your YouTube API key:
   ```toml
   [secrets]
   YOUTUBE_API_KEY = "AIzaSyCoHWffJRoJOvFmsa3JAfELkQDWeByD-9M"
   ```

## Option 2: Heroku

### Steps:
1. **Create Heroku files:**
   - `Procfile`: `web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`
   - `runtime.txt`: `python-3.11.0`

2. **Deploy:**
   ```bash
   heroku create ytgraphx-app
   git push heroku main
   ```

## Option 3: Railway

### Steps:
1. **Connect GitHub repository**
2. **Set environment variables**
3. **Deploy automatically**

## Option 4: Local Network Sharing

### Steps:
1. **Find your IP:**
   ```bash
   ipconfig
   ```

2. **Run with network access:**
   ```bash
   streamlit run streamlit_app.py --server.address 0.0.0.0
   ```

3. **Share the Network URL** (shown in terminal)

## Option 5: Docker Container

### Steps:
1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8501
   CMD ["streamlit", "run", "streamlit_app.py", "--server.address", "0.0.0.0"]
   ```

2. **Build and run:**
   ```bash
   docker build -t ytgraphx .
   docker run -p 8501:8501 ytgraphx
   ```

## 🔧 Environment Variables

For production deployment, set these environment variables:
- `YOUTUBE_API_KEY`: Your YouTube Data API v3 key
- `STREAMLIT_SERVER_PORT`: 8501 (default)
- `STREAMLIT_SERVER_ADDRESS`: 0.0.0.0 (for external access)

## 📝 Pre-deployment Checklist

- [ ] Test locally with `streamlit run streamlit_app.py`
- [ ] Verify API key works
- [ ] Check all dependencies in requirements.txt
- [ ] Test with different YouTube channels
- [ ] Ensure no hardcoded paths

## 🌐 Recommended: Streamlit Cloud

**Why Streamlit Cloud?**
- ✅ Free hosting
- ✅ Automatic GitHub integration
- ✅ Easy environment variable management
- ✅ Automatic updates on git push
- ✅ Custom domain support
- ✅ Built for Streamlit apps

**Your app will be available at:**
`https://YOUR_USERNAME-ytgraphx.streamlit.app`
