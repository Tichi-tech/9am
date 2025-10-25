# How to Demo Therapist Copilot

**TL;DR:** Run `python backend/live_demo.py` - it shows the magic! ✨

## 🎯 Which Demo Should I Use?

### For Non-Technical People (Therapists, Stakeholders, Investors)

**Use: `live_demo.py`** ← **START HERE**

```bash
cd backend
python live_demo.py
```

**What it shows:**
- "Watch it happen" experience
- Paste a journal entry → Get AI insights
- Takes 30 seconds total
- Shows before/after clearly
- Explains the value (time saved, ROI)

**Perfect for:**
- Quick demos to therapists
- "Show me how it works" questions
- Investor pitches
- Non-technical stakeholders

---

### For Product Demos (Showing the Full App)

**Use: The Frontend Dashboard**

```bash
# Make sure servers are running
cd backend && python app.py        # Terminal 1
cd frontend && npm run dev          # Terminal 2

# Then open: http://localhost:3000
```

**What it shows:**
- Beautiful UI with 3 diverse patients
- Click through different scenarios
- See themes, patterns, clinical plans
- Multi-patient management

**Perfect for:**
- Product walkthroughs
- UX/UI showcases
- Healthcare org demos
- Integration discussions

---

### For Technical Demos (Showing the Pipeline)

**Use: `pipeline_demo.py`**

```bash
cd backend
python pipeline_demo.py
```

**What it shows:**
- Complete technical pipeline
- API calls in action
- Data aggregation process
- Multi-patient system
- Full analysis workflow

**Perfect for:**
- Developer audiences
- Technical stakeholders
- API integration discussions
- Architecture reviews

---

## 🚀 Quick Start Demo Script

### Setup (One-time, 2 minutes)

```bash
# 1. Make sure you have data
cd backend
python generate_multi_patient_demo.py
python generate_analyses.py

# 2. Start backend
python app.py
```

### The Demo (30 seconds to wow them)

```bash
# In a new terminal
cd backend
python live_demo.py
```

**Follow these steps in the interactive demo:**

1. **Choose option 1** (Anxiety scenario) or 3 (Improvement)
2. **Press ENTER** to show the raw journal entry
3. **Press ENTER** to process it
4. **Press ENTER** to send to AI
5. **Watch the magic** - AI analyzes in 3-5 seconds
6. **Press ENTER** to see results:
   - Primary theme detected
   - Clinical action items
   - Specific recommendations
7. **Press ENTER** to see the value:
   - Time saved: 25-40 minutes per patient
   - Cost: $0.01-0.03
   - ROI: 2,000x

**Done!** You just showed the entire value prop in 30 seconds.

---

## 💡 Demo Tips

### Before You Start

✅ **DO:**
- Have backend running (`python app.py`)
- Test it once yourself first
- Know which scenario you'll demo (Anxiety = most dramatic)
- Have talking points ready

❌ **DON'T:**
- Forget to start the backend server
- Skip the value proposition at the end
- Oversell - "augments therapists" not "replaces"

### During the Demo

**Opening line:**
> "Let me show you what happens when a patient writes a journal entry. This is what they write..."

**After showing journal:**
> "In a traditional practice, the therapist would spend 30-45 minutes reading this, identifying patterns, preparing notes. Watch what happens with our system..."

**After AI analysis:**
> "Three seconds. That's all it took. And look at what it found - [point to specific insights]. This is what the therapist sees before the session."

**Closing:**
> "So instead of 40 minutes of prep work per patient, it's now 5 minutes. For a therapist with 20 patients, that's 11+ hours saved per week. That's $1,300 in therapist time vs 60 cents in AI costs. But more importantly - better prep means better sessions means better patient outcomes."

### Common Questions

**Q: "Does this replace the therapist?"**
A: "No! This is like spell-check for Microsoft Word - it helps the professional do their job better. The therapist still leads the session, builds the relationship, applies clinical expertise. This just saves them hours of data analysis."

**Q: "What about privacy/HIPAA?"**
A: "Great question. The current demo uses anonymized data. For production, we have a complete HIPAA compliance roadmap including encryption, audit logs, and data isolation."

**Q: "What if the AI is wrong?"**
A: "The AI provides insights, not diagnoses. Think of it like a smart assistant that says 'hey, you might want to explore this pattern.' The therapist reviews everything and makes all clinical decisions."

**Q: "How much does it cost?"**
A: "AI analysis costs $0.01-0.03 per entry. For a typical therapist with 20 patients, that's about $20-30/month total. We save them 40+ hours per month. The ROI is massive."

---

## 🎪 Sample Demo Scenarios

### Scenario 1: Anxious Patient Making Progress

**Use:** Option 3 (Improvement) in `live_demo.py`

**Talking points:**
- "Notice the mixed emotions - anxiety but also hope"
- "AI detects the therapy techniques actually working"
- "Gives therapist specific wins to reinforce"

### Scenario 2: Someone Really Struggling

**Use:** Option 1 (Anxiety) in `live_demo.py`

**Talking points:**
- "This patient is in crisis - panic attacks, isolation"
- "AI flags severity levels - 'high' for work anxiety"
- "Gives therapist immediate action items"

### Scenario 3: Complex Emotional Processing

**Use:** Option 2 (Depression) in `live_demo.py`

**Talking points:**
- "Notice the nuance - self-awareness mixed with hopelessness"
- "AI picks up on the ambivalence about therapy"
- "Helps therapist address that directly"

---

## 📊 The Numbers (Memorize These)

**Time Saved:**
- Traditional prep: 30-45 min/patient
- With AI: 5 min/patient
- Savings: 25-40 min per patient (85-90%)
- For 20 patients: 11+ hours/week saved

**Money Saved:**
- AI cost: $0.01-0.03 per analysis
- Therapist time: $100/hour average
- Weekly savings: $1,300 vs $0.60
- ROI: 2,000x - 4,000x

**Market:**
- 200K+ therapists in US
- Average caseload: 20-30 patients
- Mental health crisis growing
- Therapist shortage critical

**Pricing (if asked):**
- $50-100/month per therapist (SaaS)
- Or $500-1000/month for group practices
- Enterprise pricing for healthcare orgs

---

## 🎬 Advanced: The Full Pitch Demo (5 minutes)

For investor meetings or formal presentations:

1. **Problem (30 sec):**
   - "200K therapists in US, each spending 10-15 hours/week on manual journal review"
   - "That's 2-3 billion hours annually of tedious data analysis"
   - "Meanwhile, mental health crisis growing, therapist shortage critical"

2. **Solution - Live Demo (2 min):**
   - Run `live_demo.py`
   - Show the before/after
   - Highlight the insights

3. **Value (1 min):**
   - Time saved numbers
   - ROI calculation
   - Better outcomes testimonial (hypothetical: "Therapists report 30% better session prep")

4. **Market (30 sec):**
   - "$250B mental health industry"
   - "200K therapists, 20M+ patients"
   - "SaaS model, sticky product"

5. **Traction (30 sec):**
   - "Working prototype with 3 patient scenarios"
   - "AI analysis accuracy [X]%"
   - "Ready for pilot programs"

6. **Ask (30 sec):**
   - "Seeking [X] to build HIPAA-compliant platform"
   - "Launch pilot with 50 therapists"
   - "Path to 10K therapists in 18 months"

---

## 🆘 Troubleshooting

**"Server not responding"**
```bash
curl http://localhost:5050/health
# If fails, restart: python backend/app.py
```

**"OpenAI error"**
- Check `.env` file has `OPENAI_API_KEY`
- Note: Viewing existing analyses works without API key

**"No patients showing"**
```bash
cd backend
python generate_multi_patient_demo.py
```

**"Want different journal text"**
- Choose option 4 (custom) in `live_demo.py`
- Or edit the examples in `live_demo.py`

---

## 📞 Demo Support

**Quick Reference:**
- Frontend: http://localhost:3000
- Backend: http://localhost:5050
- Health check: http://localhost:5050/health
- API docs: `SUPER_SIMPLE_API.md`

**Files:**
- `live_demo.py` - Interactive before/after demo
- `pipeline_demo.py` - Technical pipeline demo
- `DEMO_GUIDE.md` - Detailed demo scripts

---

Remember: **The best demo is the one that shows transformation**. Raw text → Insights in seconds. That's the magic! ✨
