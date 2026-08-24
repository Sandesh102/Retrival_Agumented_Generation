# 🚀 1-Click Free Deployment Guide

This guide explains how to deploy your **RAG Document Intelligence Web Application** for free on **Streamlit Community Cloud** or **Render**.

---

## Option 1: Deploy on Streamlit Community Cloud (Recommended & 100% Free)

Streamlit Community Cloud is the fastest and easiest way to host this application for free.

### Step 1: Push Project to GitHub
1. Create a new repository on [GitHub](https://github.com/).
2. Push your project code to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Deploy RAG Web App"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.name.git
   git push -u origin main
   ```

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
2. Click **"New app"**.
3. Select your GitHub repository, set `main` branch, and set Main file path to: `app.py`.
4. Expand **Advanced settings...** $\rightarrow$ **Secrets**.
5. Add your Gemini API key in the Secrets box:
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ```
6. Click **Deploy!** 🚀

Your app will be live in 1-2 minutes with a shareable public URL for recruiters!

---

## Option 2: Deploy on Render

1. Sign up at [render.com](https://render.com/).
2. Click **New +** $\rightarrow$ **Web Service**.
3. Connect your GitHub repository.
4. Set the following settings:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5. Under **Environment Variables**, add:
   - Key: `GEMINI_API_KEY`
   - Value: `your_gemini_api_key_here`
6. Click **Create Web Service**.

---

## 🔒 Security Note
* Your `.env` file is included in `.gitignore` so your secret API key will **never** be exposed in public GitHub commits.
* Users and recruiters opening your deployed app can read the pre-loaded PDF and ask questions, with zero configuration required!
