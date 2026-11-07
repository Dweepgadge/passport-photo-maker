# PassportAI • Android APK Build Guide

There are two straightforward ways to generate a native Android `.apk` or Google Play `.aab` package from this project:

---

## Method 1: Instant 1-Click APK Generation (Recommended & No Setup Required)

Microsoft provides **PWABuilder** (free and open-source), which converts PWA-enabled projects directly into signed native Android APKs:

1. **Host or Tunnel Your App**:
   - Either deploy your app (e.g. Render, Railway, Vercel, VPS) OR create a free temporary live tunnel on your PC using Cloudflare Tunnel or ngrok:
     ```bash
     # Example with ngrok or cloudflared
     cloudflared tunnel --url http://localhost:8000
     ```
2. **Generate APK**:
   - Open **[https://www.pwabuilder.com/](https://www.pwabuilder.com/)**.
   - Paste your app URL.
   - PWABuilder will automatically read `manifest.json`, the 192x192 & 512x512 icons, and service worker.
   - Click **"Package for Stores"** $\rightarrow$ select **"Android"**.
   - Click **"Generate APK / Package"** $\rightarrow$ Download your `.apk` file!
3. Transfer the `.apk` to any Android phone and tap to install!

---

## Method 2: Native Android Studio Build (Capacitor)

If you prefer building locally via Android Studio:

1. **Install Node.js & Capacitor CLI**:
   ```bash
   npm install -g @capacitor/cli @capacitor/core @capacitor/android
   ```
2. **Initialize & Sync**:
   ```bash
   cd C:\Users\lenovo\.gemini\antigravity\scratch\passport-photo-maker
   npx cap add android
   npx cap copy
   ```
3. **Open in Android Studio**:
   ```bash
   npx cap open android
   ```
4. In Android Studio:
   - Go to **Build** $\rightarrow$ **Build Bundle(s) / APK(s)** $\rightarrow$ **Build APK(s)**.
   - Locate your `.apk` in `android/app/build/outputs/apk/debug/app-debug.apk`.

---

## Method 3: Instant Phone Installation Without Any APK (PWA)

You don't even need to compile an APK to install it on your phone:
1. Ensure your PC and phone are on the same Wi-Fi network.
2. Find your PC local IP (e.g. `192.168.1.X`).
3. Open `http://192.168.1.X:8000` in Chrome on Android or Safari on iPhone.
4. Tap the **"📲 Install App"** button at the top, or tap Chrome Menu (3 dots) $\rightarrow$ **"Add to Home screen"** / **"Install app"**.
5. The app will install directly with full-screen standalone experience, app icon, and native camera access!
