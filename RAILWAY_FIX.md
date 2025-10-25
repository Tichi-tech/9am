# Railway Build Error Fix

If you're getting "pip not found" error, here's how to fix it:

## Option 1: Simplest Fix - Root Directory Configuration

Tell Railway explicitly where each service is:

### For Backend Service:

1. In Railway dashboard, click on **backend service**
2. Go to **Settings** tab
3. Find **"Root Directory"**
4. Set it to: `backend`
5. Find **"Build Command"**
6. Set it to: `pip install -r requirements.txt`
7. Find **"Start Command"**
8. Set it to: `gunicorn app:app --bind 0.0.0.0:$PORT`
9. Click **"Redeploy"**

### For Frontend Service:

1. In Railway dashboard, click on **frontend service**
2. Go to **Settings** tab
3. Find **"Root Directory"**
4. Set it to: `frontend`
5. Find **"Build Command"**
6. Set it to: `npm install && npm run build`
7. Find **"Start Command"**
8. Set it to: `npm run preview -- --port $PORT --host 0.0.0.0`
9. Click **"Redeploy"**

---

## Option 2: If That Doesn't Work - Use Docker

Railway works better with Docker sometimes. Here's the config:

### Backend Dockerfile (already created):

See `backend/Dockerfile`

### Frontend Dockerfile (already created):

See `frontend/Dockerfile`

**In Railway:**
1. Go to service Settings
2. Change "Builder" from "Nixpacks" to "Dockerfile"
3. Set "Dockerfile Path" to `backend/Dockerfile` or `frontend/Dockerfile`
4. Redeploy

---

## Option 3: Check Python Version

If pip still not found:

1. Go to backend Settings
2. Add environment variable:
   - `NIXPACKS_PYTHON_VERSION` = `3.10`
3. Redeploy

---

## Still Not Working? Alternative Deploy Method

Deploy each service separately:

### Backend Only:

1. Create new project
2. Deploy from GitHub
3. Select "backend" folder only
4. Railway should detect Python automatically

### Frontend Only:

1. Create new project
2. Deploy from GitHub
3. Select "frontend" folder only
4. Railway should detect Node automatically

Then connect them via environment variables!

---

## Quick Test

Before deploying, test locally:

```bash
# Backend
cd backend
pip install -r requirements.txt
gunicorn app:app

# Frontend
cd frontend
npm install
npm run build
npm run preview
```

If those work, Railway should work too!
