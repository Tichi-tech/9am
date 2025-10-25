# Deployment Guide for Therapist Copilot

## Overview

This guide shows you how to deploy Therapist Copilot and create a shareable demo link.

---

## Quick Demo Setup (Local)

### For Hackathon/Immediate Demo

```bash
# 1. Generate sample data
cd backend
python demo_data_generator.py

# 2. Start Flask server
python app.py

# 3. In another terminal, run the demo
python run_demo.py

# 4. Open the dashboard
# Open frontend/demo/index.html in your browser
```

**You now have:**
- ✅ 4 weeks of realistic journal data
- ✅ Analyzed patterns showing progression
- ✅ Beautiful dashboard visualization
- ✅ All analysis saved to `data/` folder

---

## Deployment Options for Shareable Link

### Option 1: Render.com (Recommended - Free & Easy)

**Backend Deployment:**

1. **Create `render.yaml`** (already in repo):
```yaml
services:
  - type: web
    name: therapist-copilot-api
    env: python
    buildCommand: pip install -r backend/requirements.txt
    startCommand: cd backend && python app.py
    envVars:
      - key: OPENAI_API_KEY
        sync: false
```

2. **Deploy:**
   - Push code to GitHub
   - Go to [render.com](https://render.com)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repo
   - Add `OPENAI_API_KEY` in environment variables
   - Deploy! 🚀

3. **Get your API URL:**
   - After deployment: `https://therapist-copilot-api.onrender.com`

**Frontend Deployment:**

1. Update `frontend/demo/index.html`:
   - Change `BASE_URL` to your Render API URL

2. Deploy to Netlify/Vercel (free):
   - Drag & drop `frontend/demo` folder
   - Get instant link: `https://therapist-copilot-demo.netlify.app`

**Total Time:** ~15 minutes
**Cost:** FREE

---

### Option 2: Railway.app (Easiest)

1. **Install Railway CLI:**
```bash
npm install -g @railway/cli
```

2. **Deploy:**
```bash
railway login
railway init
railway up
```

3. **Set environment variable:**
```bash
railway variables set OPENAI_API_KEY=sk-your-key
```

4. **Get public URL:**
```bash
railway domain
```

**Total Time:** ~5 minutes
**Cost:** FREE (with credits)

---

### Option 3: Heroku

1. **Create `Procfile`:**
```
web: cd backend && python app.py
```

2. **Deploy:**
```bash
heroku login
heroku create therapist-copilot
git push heroku main
heroku config:set OPENAI_API_KEY=sk-your-key
heroku open
```

**Total Time:** ~10 minutes
**Cost:** $7/month (Eco dyno)

---

### Option 4: DigitalOcean App Platform

1. **Connect GitHub repo**
2. **Configure:**
   - Type: Web Service
   - Build Command: `pip install -r backend/requirements.txt`
   - Run Command: `cd backend && python app.py`
   - Add env var: `OPENAI_API_KEY`

3. **Deploy & get URL**

**Total Time:** ~10 minutes
**Cost:** $5/month

---

## Frontend-Only Quick Demo

If you just need a shareable dashboard without live backend:

### Option A: GitHub Pages

```bash
cd frontend/demo

# Update index.html to use demo data (already configured)

git add .
git commit -m "Add demo dashboard"
git push

# Enable GitHub Pages in repo settings
# Point to /frontend/demo directory
```

**Link:** `https://yourusername.github.io/9am`

### Option B: Netlify Drop

1. Go to [app.netlify.com/drop](https://app.netlify.com/drop)
2. Drag & drop `frontend/demo` folder
3. Get instant link!

**Time:** 30 seconds

---

## Running the Value Demo

### Step 1: Generate Demo Data

```bash
cd backend
python demo_data_generator.py
```

This creates 4 weeks of journal entries showing realistic patient progression:
- **Week 1:** High anxiety, isolation, panic attacks
- **Week 2:** Learning coping strategies
- **Week 3:** Testing boundaries, mixed results
- **Week 4:** Significant improvement, active engagement

### Step 2: Analyze the Data

```bash
# Make sure server is running
python app.py

# In another terminal, run demo script
python run_demo.py
```

The demo will:
1. Analyze Week 1 (baseline anxiety)
2. Analyze Week 4 (showing progress)
3. Run long-term analysis (full month)
4. Display value proposition

### Step 3: Show the Dashboard

Open `frontend/demo/index.html` in a browser to see:
- 📈 Mood trajectory chart (visual improvement)
- 🎯 Key patterns with severity levels
- 📅 Week-by-week progress timeline
- 💡 Clinical action items
- ✨ Treatment progress indicator (78%)

---

## Demo Script for Stakeholders

### Opening (1 minute)

"Therapists spend 30-45 minutes before each session reviewing patient journals and notes. Therapist Copilot analyzes journal entries using AI, providing instant insights."

### Weekly Analysis Demo (2 minutes)

"Here's a patient's first week of therapy. The AI identifies:
- High anxiety and social avoidance
- Daily panic attacks
- Specific clinical prompts for the next session

This took 5 seconds. Manually, it would take 30 minutes."

### Long-term Value Demo (3 minutes)

"Now watch what happens over a month..."

[Show dashboard with progression chart]

"The system tracked:
- Sentiment improving from -0.45 to +0.15
- Panic attacks: daily → occasional
- Social engagement: isolated → active
- Treatment effectiveness: 78% progress

This gives therapists **data-driven proof** that therapy is working."

### ROI Pitch (1 minute)

"**Time saved:** 30-45 min/week = 2-3 hours/month
**Cost:** $0.01-0.03 per analysis
**Value:** Better patient outcomes, reduced therapist burnout, quantifiable progress

For a therapist seeing 20 patients, that's **40-60 hours saved monthly.**"

---

## What to Show

### For Technical Audience:
- API endpoints and data flow
- ChatGPT analysis quality
- Long-term trend detection
- Scalability (handles months/years of data)

### For Clinical Audience:
- Pattern detection accuracy
- Clinical prompts usefulness
- Progress visualization
- How it complements (not replaces) clinical judgment

### For Business Audience:
- Time savings ROI
- Cost per analysis
- Scalability
- Market opportunity (mental health crisis + therapist shortage)

---

## Files Needed for Demo

### Must Have:
- ✅ `backend/demo_data_generator.py` - Sample data
- ✅ `backend/run_demo.py` - Demo script
- ✅ `frontend/demo/index.html` - Dashboard
- ✅ `BACKEND_SUMMARY.md` - Technical docs

### Nice to Have:
- 📊 PowerPoint with key stats
- 🎥 Screen recording of demo
- 📝 One-pager PDF for investors

---

## Troubleshooting

### "Cannot connect to server"
```bash
# Make sure Flask is running
cd backend
python app.py
```

### "OpenAI API error"
```bash
# Check your .env file
cd backend
cat .env  # Should show OPENAI_API_KEY=sk-...
```

### "No data files found"
```bash
# Generate demo data first
python demo_data_generator.py
```

### "Port 5000 already in use"
```bash
# Change port
PORT=5001 python app.py
# Update BASE_URL in demo scripts to :5001
```

---

## Next Steps After Demo

### Immediate (This Week):
1. Generate 4 weeks of demo data
2. Run analysis and save results
3. Deploy dashboard to free hosting
4. Share link with team/stakeholders

### Short-term (Next Month):
1. Collect real therapist feedback
2. Refine prompts based on clinical input
3. Add more visualization options
4. Implement authentication

### Long-term (Future):
1. HIPAA compliance
2. Multi-patient management
3. Custom report generation
4. Integration with EMR systems

---

## Support

**Questions?** Create an issue in the GitHub repo or check:
- `README.md` - Project overview
- `BACKEND_SUMMARY.md` - Technical details
- `backend/README.md` - API documentation

---

## Quick Reference

**Generate data:**
```bash
python demo_data_generator.py
```

**Run backend:**
```bash
python app.py
```

**Run demo:**
```bash
python run_demo.py
```

**View dashboard:**
```
open frontend/demo/index.html
```

**Deploy to web:**
- Easiest: Netlify Drop (frontend only)
- Best: Render.com (full stack)
- Fastest: Railway.app

---

🚀 **Ready to showcase your demo!**
