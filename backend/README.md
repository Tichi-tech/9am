# Therapist Copilot - Backend API

Flask-based backend for analyzing patient journal entries using OpenAI GPT-4.

## Quick Start

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.sample .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-...your-key-here
FRONTEND_URL=http://localhost:3000
```

### 3. Run the Server

```bash
python app.py
```

Server will run at `http://localhost:5050`

---

## API Endpoints

### Health Check
```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "Therapist Copilot Backend API is running"
}
```

---

### Convert Google Doc to JSON
```
POST /api/convert-google-doc
```

**Request Body:**
```json
{
  "doc_url": "https://docs.google.com/document/d/...",
  "date": "2025-01-12"
}
```

For MVP testing without Google Docs API:
```json
{
  "doc_url": "Journal entry text goes here...",
  "date": "2025-01-12"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Entry converted and saved",
  "entry": {
    "date": "2025-01-12",
    "time": "22:30",
    "text": "..."
  },
  "file": "2025-01-12.json"
}
```

---

### Aggregate Weekly Entries
```
POST /api/aggregate-week
```

**Request Body:**
```json
{
  "week_start": "2025-01-12",
  "week_end": "2025-01-18"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Weekly entries aggregated",
  "entry_count": 7,
  "file": "week_2025-01-12_to_2025-01-18.json",
  "weekly_data": { ... }
}
```

---

### Analyze Weekly Entries
```
POST /api/analyze-week
```

**Request Body:**
```json
{
  "week_start": "2025-01-12",
  "week_end": "2025-01-18"
}
```

**Response:**
```json
{
  "success": true,
  "theme": "Difficulty Setting Boundaries",
  "summary": {
    "week_period": "2025-01-12 to 2025-01-18",
    "patterns": [...],
    "mood_trends": {...},
    "key_topics": [...],
    "clinical_prompts": [...]
  }
}
```

---

### Full Pipeline (Recommended for MVP)
```
POST /api/process-full-pipeline
```

Converts docs → aggregates → analyzes in one call.

**Request Body:**
```json
{
  "doc_urls": [
    {"url": "Entry text 1...", "date": "2025-01-12"},
    {"url": "Entry text 2...", "date": "2025-01-13"}
  ],
  "week_start": "2025-01-12",
  "week_end": "2025-01-18"
}
```

---

### List Patients (Frontend helper)
```
GET /api/patients
```

Returns registered patients plus basic metadata (name, entry counts, latest analyzed week). Uses `data/patients.json` when available or discovers folders in `data/`.

---

### Fetch Stored Weekly Analyses (Frontend helper)
```
GET /api/patients/<patient_id>/analyses
```

Reads any `summary_*.json` files saved for the patient and normalizes the data for the React dashboard. The latest entry is returned first.

---

### Offline Full Pipeline Script
```
python scripts/full_pipeline.py \
    --patient-id maya-thompson \
    --week-start 2025-01-12 \
    --week-end 2025-01-18 \
    --entries-file data/maya-thompson/new_entries.json
```

The script ingests a batch of daily journal JSON, aggregates the requested week, runs `analyze_weekly_entries`, and writes both the summary JSON plus a therapist-facing Markdown report under `data/<patient_id>/`.

---

## Testing with Sample Data

### Quick Test Script

```bash
# Start the server
python app.py

# In another terminal, test with curl:
curl -X POST http://localhost:5050/api/convert-google-doc \
  -H "Content-Type: application/json" \
  -d '{
    "doc_url": "I felt overwhelmed today...",
    "date": "2025-01-12"
  }'
```

### Using Python Requests

```python
import requests
import json

# Load test data
with open('test_data.json', 'r') as f:
    test_data = json.load(f)

# Full pipeline test
response = requests.post('http://localhost:5050/api/process-full-pipeline', json={
    "doc_urls": [
        {"url": entry["text"], "date": entry["date"]}
        for entry in test_data["sample_entries"]
    ],
    "week_start": "2025-01-12",
    "week_end": "2025-01-18"
})

print(json.dumps(response.json(), indent=2))
```

---

## File Structure

```
backend/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.sample                 # Environment template
├── test_data.json             # Sample journal entries
├── README.md                  # This file
├── prompts/
│   └── analysis_prompt.txt    # GPT-4 analysis prompt
└── utils/
    ├── __init__.py
    ├── google_doc_converter.py  # Doc → JSON converter
    └── analyzer.py              # GPT-4 analysis logic
```

---

## Data Flow

```
1. Google Doc/Text Input
   ↓
2. convert_google_doc_to_json() → daily JSON files
   ↓
3. aggregate_week() → weekly JSON file
   ↓
4. analyze_weekly_entries() → ChatGPT analysis
   ↓
5. POST to Frontend → Display insights
```

---

## Troubleshooting

### "OPENAI_API_KEY not found"
- Make sure `.env` file exists in `backend/` directory
- Check that `OPENAI_API_KEY=sk-...` is set correctly
- Restart the Flask server after editing `.env`

### "Google Docs credentials not found"
For MVP testing, pass plain text instead of Google Doc URLs:
```json
{"doc_url": "Plain text entry...", "date": "2025-01-12"}
```

To use real Google Docs:
1. Go to Google Cloud Console
2. Enable Google Docs API
3. Download `credentials.json`
4. Place in `backend/` directory

### "Module not found" errors
```bash
pip install -r requirements.txt
```

---

## Development Notes

### For MVP Demo
- Use `test_data.json` for sample entries
- Use `/api/process-full-pipeline` for simplest testing
- Google Docs integration is optional for MVP

### For Production
- Implement proper authentication
- Use Google service accounts (not OAuth)
- Add rate limiting
- Implement HIPAA-compliant data encryption
- Add comprehensive error handling
- Set up logging and monitoring

---

## Next Steps

1. **Frontend Integration**: POST analysis results to frontend dashboard
2. **Real-time Processing**: Add webhook support for automatic analysis
3. **Multi-patient Support**: Add patient ID routing
4. **Export Features**: Generate PDF reports from analysis

---

## Contact

Questions? Check the main project README or create an issue.
