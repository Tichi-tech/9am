# Railway Deployment Guide

Deploy Therapist Copilot to Railway in 5 minutes!

## 🚀 Quick Start

### Step 1: Push to GitHub (if not already)

```bash
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

### Step 2: Deploy to Railway

1. **Go to https://railway.app**

2. **Sign up with GitHub** (easiest way)

3. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your repos
   - Select this repository

4. **Railway will detect 2 services**:
   - ✅ Backend (Python/Flask)
   - ✅ Frontend (Node/React)

### Step 3: Configure Backend

1. Click on the **Backend service**

2. **Add Environment Variables**:
   - Click "Variables" tab
   - Add: `OPENAI_API_KEY` = `your-actual-key-here`
   - Add: `PORT` = `5050` (Railway will override this automatically)

3. **Generate Domain**:
   - Click "Settings" tab
   - Scroll to "Networking"
   - Click "Generate Domain"
   - Copy the URL (like: `therapist-backend-production.up.railway.app`)

### Step 4: Configure Frontend

1. Click on the **Frontend service**

2. **Add Environment Variable**:
   - Click "Variables" tab
   - Add: `VITE_API_BASE_URL` = `https://YOUR-BACKEND-URL.railway.app`
   - (Use the backend URL from step 3)

3. **Generate Domain**:
   - Click "Settings" tab
   - Scroll to "Networking"
   - Click "Generate Domain"
   - **This is your link for judges!** 🎉

### Step 5: Wait for Deployment

- Watch the deployment logs
- Backend: ~2-3 minutes
- Frontend: ~1-2 minutes
- Both turn green when ready ✅

### Step 6: Test Your Link

Open your frontend URL and verify:
- ✅ Demo tab loads
- ✅ Can click "Run AI Analysis"
- ✅ Patient list appears
- ✅ Can switch between patients

---

## 🎯 Your Live Links

After deployment, you'll have:

**Frontend (Share This!)**: `https://therapist-copilot-production.up.railway.app`

**Backend**: `https://therapist-backend-production.up.railway.app`

**Health Check**: `https://therapist-backend-production.up.railway.app/health`

---

## 🔧 Troubleshooting

### "Backend not responding"

Check environment variables:
1. Go to backend service → Variables
2. Verify `OPENAI_API_KEY` is set
3. Click "Redeploy"

### "Frontend shows errors"

Check API URL:
1. Go to frontend service → Variables
2. Verify `VITE_API_BASE_URL` points to backend
3. Make sure it starts with `https://`
4. Click "Redeploy"

### "Need to redeploy"

```bash
# Make a change, then:
git add .
git commit -m "Update"
git push origin main

# Railway auto-redeploys!
```

---

## 💡 Tips for Judges

**Your submission link**: The frontend URL

**What to tell judges**:
- "Click the ✨ Demo tab"
- "Press 'Run AI Analysis' to see the magic"
- "Then explore the 3 patient profiles"
- "Check out Summary, Theme, and Plan tabs"

**If demo is slow first time**:
- Railway spins up from cold start
- Takes 5-10 seconds on first load
- Tell judges: "First load might take a moment"

---

## 🎉 You're Done!

Your app is now live at:
`https://your-frontend.railway.app`

**No cooldown. No sleep. Fast and reliable!**

Share the link with your judges and good luck! 🏆
