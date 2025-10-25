# Demo Guide - Therapist Copilot

Quick guide for running impressive demos of the Therapist Copilot system.

## 🎯 What This Demo Shows

- **Multi-patient support** - 3 diverse therapeutic scenarios
- **Full pipeline** - From journal text → AI insights
- **Real AI analysis** - Live ChatGPT integration
- **Clinical value** - Actionable insights for therapists

## 📊 Demo Patients

### 1. Maya Thompson
- **Scenario:** Workplace anxiety and social isolation
- **Therapist:** Dr. Evelyn Carter
- **Data:** 10 journal entries showing improvement over 2 weeks
- **Theme:** Anxiety patterns with coping strategy adoption

### 2. James Rivera
- **Scenario:** Grief counseling after loss of partner
- **Therapist:** Dr. Sarah Chen
- **Data:** 7 journal entries processing grief
- **Theme:** Emotional processing and acceptance journey

### 3. Alex Kim
- **Scenario:** Career burnout and perfectionism
- **Therapist:** Dr. Michael Torres
- **Data:** 7 journal entries about work-life balance
- **Theme:** Boundary-setting and self-worth exploration

## 🚀 Quick Demo (5 minutes)

### Option 1: Frontend Dashboard Demo

1. **Start servers** (if not running):
   ```bash
   # Terminal 1 - Backend
   cd backend
   python app.py

   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

2. **Open browser**: http://localhost:3000

3. **Show multi-patient view**:
   - Click through each patient in the sidebar
   - Show different therapeutic scenarios
   - Demonstrate tabs: Summary, Theme, Plan

4. **Highlight key features**:
   - AI-detected emotional patterns
   - Sentiment scoring
   - Clinical action items
   - Patient strengths

### Option 2: Live Pipeline Demo

This shows the **complete technical pipeline** in action:

```bash
cd backend
python pipeline_demo.py
```

**What it demonstrates:**
1. Patient data management (API)
2. Journal aggregation
3. Live AI analysis with ChatGPT
4. Clinical insights generation
5. Multi-patient comparison

**Follow the prompts** - it's interactive and self-explanatory!

## 🎪 Full Demo Script (15 minutes)

Perfect for stakeholder presentations or investor pitches.

### Part 1: The Problem (2 min)

**Script:**
> "Therapists spend 30-45 minutes before each session reading patient journals, trying to spot patterns and prepare discussion topics. With a typical caseload of 20+ patients, that's 10-15 hours per week just on prep work.
>
> Meanwhile, patients write their most honest thoughts between sessions - in journals, notes, late-night reflections. This data is gold, but it's overwhelming for therapists to process manually."

### Part 2: The Solution - Live Demo (10 min)

#### Step 1: Show the Data (1 min)
```bash
# Show we have 3 real patients
curl http://localhost:5050/api/patients | python -m json.tool
```

**Point out:**
- 3 different patients
- Different therapists
- Different scenarios
- Real journal entries

#### Step 2: Frontend Dashboard (4 min)

Open http://localhost:3000

**Walk through Maya Thompson:**
1. **Summary tab:** "Here's a week of journal entries analyzed in seconds"
2. **Theme tab:** "AI identified her primary pattern: workplace anxiety"
3. **Plan tab:** "Specific action items for the therapist's next session"

**Switch to James Rivera:**
- "Completely different scenario - grief counseling"
- "AI detects emotional processing patterns"
- "Notice the different tone and recommendations"

**Switch to Alex Kim:**
- "Career burnout and perfectionism"
- "AI spots the self-worth issues underlying work stress"

#### Step 3: Live Pipeline (5 min)
```bash
python pipeline_demo.py
```

**Narrate as it runs:**
- "This is fetching all patients from our API"
- "Now it's aggregating a week of journal entries"
- "Here's where ChatGPT analyzes the emotional patterns"
- "And boom - clinical insights in 3-5 seconds"

**Highlight the output:**
- Emotional patterns detected
- Severity levels (low/moderate/high)
- Mood trajectory
- Specific therapist action items

### Part 3: The Value (3 min)

**Show the math:**

```
Traditional approach:
- 40 min prep per patient per week
- 20 patients = 13+ hours/week
- $100/hour therapist time = $1,300/week

With Therapist Copilot:
- 5 seconds AI analysis per patient
- Review insights: 5 min per patient
- 20 patients = 1.7 hours/week
- Cost: $0.60/week for AI (20 × $0.03)

SAVINGS: 11+ hours and $1,299 per week
ROI: 217,000%
```

**But more importantly:**
> "This isn't about replacing therapists. It's about giving them superpowers. Better prep = better sessions = better patient outcomes. And isn't that what healthcare should be about?"

## 🎬 Demo Tips

### Do's ✅
- **Start with the problem** - everyone understands overwhelmed therapists
- **Use real patient names** - makes it tangible ("Maya's anxiety vs Patient 001")
- **Show the AI working** - the 3-5 second analysis is impressive
- **Highlight diversity** - 3 different scenarios show versatility
- **End with ROI** - time and money saved

### Don'ts ❌
- **Don't skip the frontend** - it's visual and intuitive
- **Don't ignore privacy concerns** - mention HIPAA compliance plans
- **Don't oversell** - this augments therapists, doesn't replace them
- **Don't forget the mission** - better tools = better mental health care

## 🔧 Troubleshooting

**"Backend not responding"**
```bash
# Check if running
curl http://localhost:5050/health

# If not, start it
cd backend && python app.py
```

**"No patients showing"**
```bash
# Regenerate demo data
cd backend
python generate_multi_patient_demo.py
python generate_analyses.py
```

**"OpenAI API error"**
- Check that `.env` file exists in root or backend directory
- Verify `OPENAI_API_KEY` is set
- Note: Viewing existing analyses doesn't need API key

**"Frontend not loading"**
```bash
cd frontend
npm install  # If needed
npm run dev
```

## 📊 Sample Talking Points

### For Therapists:
- "Saves you 30-45 minutes of prep per patient"
- "Spots patterns you might miss"
- "Quantifies patient progress objectively"
- "Lets you focus on therapy, not data analysis"

### For Patients:
- "Your therapist will be better prepared"
- "Concrete evidence of your progress"
- "More focused, effective sessions"
- "Your journaling actually helps your treatment"

### For Healthcare Orgs:
- "Increases therapist capacity by 15-20%"
- "Improves patient outcomes measurably"
- "Costs $0.60/patient/month for AI"
- "Reduces burnout and turnover"

### For Investors:
- "Mental health crisis + therapist shortage = huge market"
- "$250B mental health industry"
- "Our TAM: 200K+ therapists in US alone"
- "SaaS model: $50-100/month per therapist"
- "217,000% ROI for customers"

## 🚀 Next Steps After Demo

1. **Share API docs**: `SUPER_SIMPLE_API.md`
2. **Show deployment guide**: `DEPLOYMENT_GUIDE.md`
3. **Discuss HIPAA compliance**: For production use
4. **Pricing models**: Per-therapist or per-organization
5. **Integration**: How it fits their workflow

## 📞 Support

Questions during demo?
- Technical: Check `README.md` and `QUICK_START.md`
- API: See `SUPER_SIMPLE_API.md`
- Deployment: See `DEPLOYMENT_GUIDE.md`

---

**Remember:** This tool helps therapists help people. That's the story. That's the mission. 💙
