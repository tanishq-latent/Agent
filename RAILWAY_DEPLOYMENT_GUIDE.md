# 🚂 How to Deploy This Project on Railway

Railway (`railway.app`) is the fastest and easiest way to deploy Python FastAPI applications.

---

## 📋 Step 1: Check Required Deployment Files

We have created the **[Procfile](file:///Users/tanishqvyas/Agent/Procfile)** in your project root:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## 🐙 Step 2: Push Project to GitHub

1. Open terminal in `/Users/tanishqvyas/Agent`.
2. Commit and push your code:
   ```bash
   git init
   git add .
   git commit -m "Deploy Autonomous Resume Screening Agent to Railway"
   ```
3. Push to your GitHub repository.

---

## ⚡ Step 3: Deploy on Railway

1. Go to [railway.app](https://railway.app) and sign in with GitHub.
2. Click **+ New Project** $\rightarrow$ **Deploy from GitHub repo**.
3. Select your repository (`resume-agent`).
4. Click **Deploy Now**.

---

## 🔑 Step 4: Add Environment Variables in Railway

1. In your Railway project dashboard, click on your deployed service.
2. Navigate to the **Variables** tab.
3. Click **+ New Variable** and add:
   - **Variable Name**: `GROQ_API_KEY`
   - **Value**: `gsk_your_groq_api_key_here`
4. Click **Add**.

---

## 🌐 Step 5: Generate Public Domain

1. In your Railway service dashboard, go to the **Settings** tab.
2. Scroll down to **Networking** $\rightarrow$ **Public Networking**.
3. Click **Generate Domain**.
4. Railway will generate a live HTTPS link (e.g. `https://resume-agent-production.up.railway.app`).

---

### 🎉 That's It!
Your application is live and accessible globally!
