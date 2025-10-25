# Therapist Copilot 🧠

AI-assisted emotional pattern insight from patient journaling.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Patients often write their most honest emotional reflections **outside** of therapy — in journals, notes, and late-night thoughts.
This system takes a week's worth of journal entries and helps therapists understand:

- **Recurring emotional patterns** — Identifying themes that appear across multiple entries
- **Trigger → Response → Coping cycles** — Understanding emotional cause-and-effect chains
- **Mood / language shifts** — Detecting changes in emotional tone and expression
- **Possible areas to explore in session** — Surfacing topics worth deeper therapeutic exploration

### Important Note

**We are not replacing therapy.**
We are giving therapists **clarity**, not advice. This tool is designed to augment the therapeutic relationship by providing data-driven insights that inform — not replace — clinical judgment.

---

## Architecture (Simple MVP)

```
data/journals.json → backend GPT Pattern Analyzer → data/summary.json → frontend dashboard UI
```

**Key Design Decisions:**
- No live SMS input needed for MVP
- Using example journal entries to simulate a week's emotional data
- Focus on pattern recognition and clear visualization
- Privacy-first approach (all data stays local during development)

---

## Folder Structure

```
therapist-copilot/
├── frontend/              # Therapist dashboard UI (Next.js recommended)
│   ├── components/        # Reusable UI components
│   ├── pages/            # Dashboard pages
│   └── styles/           # CSS/styling
├── backend/              # Pattern extraction logic (Python)
│   ├── analyzer.py       # Core GPT pattern analysis
│   ├── prompts/          # Prompt templates
│   └── utils/            # Helper functions
├── data/
│   ├── journals.json     # Example patient journals (team writes this)
│   └── summary.json      # Output summary for UI display
├── tests/                # Unit and integration tests
├── docs/                 # Additional documentation
├── .env.example          # Environment variable template
├── .gitignore
├── README.md
└── requirements.txt      # Python dependencies
```

---

## Team Roles

| Name | Focus | Output | Responsibilities |
|------|-------|--------|------------------|
| **UI Lead** | Frontend dashboard | Displays summary + patterns nicely | Build responsive UI, data visualization, UX design |
| **Backend Lead** | GPT logic + summarization | Generates summary.json | API integration, prompt engineering, data processing |
| **Content Contributor 1** | Writes journals.json | 10–25 emotional entries | Create realistic sample data, test edge cases |
| **Content Contributor 2** | Helps test & refine prompts | Improves pattern clarity | Quality assurance, prompt optimization |

---

## Getting Started

### Prerequisites

**Backend:**
- Python 3.8+
- OpenAI API key

**Frontend:**
- Node.js 16+ and npm/yarn
- Modern web browser

### Installation

#### 1. Clone the repository

```bash
git clone <repo_url>
cd therapist-copilot
```

#### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:
```bash
cp .env.example .env
```

Add your OpenAI API key to `.env`:
```
OPENAI_API_KEY=your_api_key_here
```

#### 3. Frontend Setup

```bash
cd frontend
npm install
# or
yarn install
```

#### 4. Add Sample Data

Create `data/journals.json` with sample entries (see format below).

---

## Usage

### Running the Backend

```bash
cd backend
python analyzer.py
```

This will:
1. Read entries from `data/journals.json`
2. Analyze patterns using GPT
3. Generate `data/summary.json`

### Running the Frontend

```bash
cd frontend
npm run dev
# or
yarn dev
```

Visit `http://localhost:3000` to view the dashboard.

---

## Data Formats

### Input: `data/journals.json`

```json
{
  "patient_id": "anonymous_001",
  "week_start": "2025-01-12",
  "week_end": "2025-01-18",
  "entries": [
    {
      "date": "2025-01-12",
      "time": "22:30",
      "text": "I felt really overwhelmed today at work. Everyone needed something from me and I couldn't say no. By the time I got home, I just wanted to disappear."
    },
    {
      "date": "2025-01-13",
      "time": "14:15",
      "text": "I wanted to reach out to Sarah but didn't. I convinced myself she's probably busy and doesn't want to hear from me anyway. Why do I always do this?"
    },
    {
      "date": "2025-01-14",
      "time": "09:00",
      "text": "Woke up feeling heavy again. This is the third day in a row. I used to love mornings."
    }
  ]
}
```

### Output: `data/summary.json`

```json
{
  "analysis_date": "2025-01-19",
  "week_period": "2025-01-12 to 2025-01-18",
  "patterns": [
    {
      "type": "recurring_theme",
      "title": "Difficulty Setting Boundaries",
      "description": "Multiple entries mention feeling unable to say 'no' to others' requests, leading to overwhelm and desire to withdraw.",
      "frequency": 3,
      "related_entries": ["2025-01-12", "2025-01-15"]
    },
    {
      "type": "emotional_cycle",
      "trigger": "Social situations or anticipated interactions",
      "response": "Self-isolation, negative self-talk",
      "coping": "Withdrawal, avoidance",
      "examples": ["2025-01-13", "2025-01-16"]
    }
  ],
  "mood_trends": {
    "overall_sentiment": "negative",
    "sentiment_score": -0.42,
    "mood_shift": "Declining through the week, particularly in mornings"
  },
  "key_topics": [
    {"topic": "work_stress", "count": 4},
    {"topic": "social_anxiety", "count": 3},
    {"topic": "sleep_quality", "count": 2}
  ],
  "clinical_prompts": [
    "Explore boundary-setting skills and assertiveness training",
    "Investigate patterns of social anxiety and avoidance",
    "Assess for depression symptoms, particularly morning mood patterns"
  ]
}
```

---

## Development Workflow

### Git Workflow

#### Before Starting Work

```bash
git pull origin main
```

#### Making Changes

1. Create a feature branch (optional but recommended):
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Test your changes locally

4. Commit with descriptive messages:
   ```bash
   git add .
   git commit -m "Add: detailed description of your changes"
   ```

5. Push to repository:
   ```bash
   git push origin main
   # or if using feature branch:
   git push origin feature/your-feature-name
   ```

### Commit Message Guidelines

- **Add:** New feature or file
- **Update:** Improvement to existing feature
- **Fix:** Bug fix
- **Refactor:** Code restructuring
- **Docs:** Documentation changes
- **Test:** Adding or updating tests

---

## Key Features for MVP Demo

### Must-Have Features

- [ ] **Sample Data Generation** — 10-25 realistic journal entries covering a week
- [ ] **Pattern Analysis** — GPT-based extraction of emotional patterns
- [ ] **Summary Generation** — Clear, structured JSON output
- [ ] **Dashboard UI** — Clean display of patterns, trends, and clinical prompts
- [ ] **Visualization** — Charts showing mood trends over time

### Nice-to-Have Features

- [ ] Multiple patient profiles
- [ ] Export summary as PDF
- [ ] Annotation/notes feature for therapists
- [ ] Severity indicators for concerning patterns

---

## Privacy & Ethics

### Data Handling
- All sample data is fictional and anonymized
- No real patient information should be used during development
- Production system must comply with HIPAA regulations
- End-to-end encryption required for any real deployment

### Ethical Considerations
- Tool provides insights, not diagnoses
- Requires human (therapist) oversight
- Should supplement, not replace, clinical judgment
- Patients should consent to journal analysis

---

## Technology Stack

### Backend
- **Language:** Python 3.8+
- **AI:** OpenAI GPT-4 API
- **Data Processing:** pandas, numpy
- **Sentiment Analysis:** TextBlob or VADER

### Frontend
- **Framework:** Next.js (React)
- **Styling:** Tailwind CSS or Material-UI
- **Charts:** Chart.js or Recharts
- **State Management:** React Context or Redux (if needed)

---

## Testing

### Backend Tests

```bash
cd backend
pytest tests/
```

### Frontend Tests

```bash
cd frontend
npm test
# or
yarn test
```

---

## Roadmap

### Phase 1: MVP (Current)
- Static journal data analysis
- Basic pattern recognition
- Simple dashboard UI

### Phase 2: Enhanced Features
- Real-time journal input (SMS/email integration)
- Multi-week trend analysis
- Therapist annotation system

### Phase 3: Production Ready
- HIPAA compliance
- User authentication
- Encrypted data storage
- Advanced ML models

---

## Contributing

1. Check existing issues or create a new one
2. Fork the repository
3. Create a feature branch
4. Make your changes with clear commit messages
5. Submit a pull request

---

## Support & Resources

### Documentation
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Next.js Documentation](https://nextjs.org/docs)
- [Python Best Practices](https://docs.python-guide.org/)

### Team Communication
- **Questions?** Post in team Slack/Discord
- **Bugs?** Create a GitHub issue
- **Ideas?** Start a discussion in the repo

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Acknowledgments

- Built during [Hackathon Name]
- Inspired by the need for better therapeutic tools
- Thanks to all contributors and testers

---

## Contact

For questions or feedback, reach out to the team leads or create an issue in this repository.

---

**Remember:** This is a tool to support therapists, not replace them. Human empathy, clinical expertise, and therapeutic relationships remain irreplaceable. 💙
