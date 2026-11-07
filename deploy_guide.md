# PassportAI • Cloud Deployment Guide (Free & Permanent)

This guide walks you through deploying your PassportAI app to the internet for free so that anyone worldwide can use it and make payments from their phone or computer.

---

## Method 1: Deploy on Render.com (Recommended Free Cloud Host)

Render provides free web hosting with automatic HTTPS SSL certificates and GitHub continuous deployment.

### Step 1: Push Code to GitHub
1. Open PowerShell or Terminal in the project directory:
   ```powershell
   cd C:\Users\lenovo\.gemini\antigravity\scratch\passport-photo-maker
   git init
   git add .
   git commit -m "Initial PassportAI release"
   ```
2. Go to [GitHub.com](https://github.com) and click **"New repository"**. Name it `passport-photo-maker` (set to Public or Private).
3. Push your code using the commands shown on GitHub:
   ```powershell
   git remote add origin https://github.com/<your-username>/passport-photo-maker.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Render.com
1. Go to **[https://render.com/](https://render.com/)** and sign up for free (using your GitHub account).
2. On the dashboard, click **"New +"** $\rightarrow$ select **"Web Service"**.
3. Choose **"Build and deploy from a Git repository"** and select your `passport-photo-maker` repository.
4. Fill in the details:
   * **Name**: `passport-ai` (or your chosen brand name)
   * **Region**: Choose the closest region (e.g. Singapore or Frankfurt)
   * **Runtime**: `Docker` *(Automatically detected from the Dockerfile)*
   * **Instance Type**: `Free`
5. *(Optional)* Add your live Razorpay keys in **Environment Variables**:
   * `RAZORPAY_KEY_ID`: `rzp_live_yourActualKey`
   * `RAZORPAY_KEY_SECRET`: `yourActualSecret`
6. Click **"Deploy Web Service"**!

Render will build the container, cache the AI model, and give you a live URL:
👉 **`https://passport-ai.onrender.com`**

---

## Method 2: Instant Public HTTPS Link (Right Now from Your PC)

If you want an instant live public URL to test on remote phones right this second without uploading to GitHub:

1. Download the free Cloudflare Tunnel tool:
   ```powershell
   winget install --id Cloudflare.cloudflared
   ```
2. Run this single command:
   ```powershell
   cloudflared tunnel --url http://localhost:8000
   ```
3. Cloudflare will print an instant public link:
   `https://random-words.trycloudflare.com`
4. Anyone on any network can open that link immediately!

---

## Method 3: Hugging Face Spaces (Free 16 GB RAM)

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces) $\rightarrow$ **"Create new Space"**.
2. Select **Docker** space (blank).
3. Push this directory using Git to Hugging Face.
4. Hugging Face allocates a dedicated free container with 2 vCPUs and 16 GB RAM.
