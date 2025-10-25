# Simple API Guide - For Your Friend 👋

## What You Get Back (3 Things!)

When you POST to the API, you get back **exactly 3 sections** in JSON:

```
┌─────────────────────────────────────────┐
│  1. THEME (string)                      │
│  → Main pattern in one sentence         │
├─────────────────────────────────────────┤
│  2. SUMMARY (object)                    │
│  → Week overview + patterns + topics    │
├─────────────────────────────────────────┤
│  3. SUGGESTIONS (array)                 │
│  → Action items for therapist           │
└─────────────────────────────────────────┘
```

---

## Example Response

```json
{
  "theme": "Feelings of Overwhelm and Inadequacy",

  "summary": {
    "week_period": "2025-01-12 to 2025-01-18",
    "entry_count": 7,
    "overall_mood": "negative",
    "sentiment_score": -0.42,
    "key_patterns": [
      {
        "pattern": "Feelings of Overwhelm",
        "severity": "moderate",
        "description": "Patient feels unable to say no..."
      },
      {
        "pattern": "Social Avoidance",
        "severity": "high",
        "description": "Avoiding interactions due to fear..."
      }
    ],
    "main_topics": ["work_stress", "anxiety", "panic_attacks"]
  },

  "suggestions": [
    "Explore boundary-setting skills",
    "Discuss social anxiety patterns",
    "Practice panic attack coping strategies"
  ]
}
```

---

## How to Use Each Section

### 1. THEME
```javascript
// Display as main heading
<h1>{response.theme}</h1>
```

**Shows:** `"Feelings of Overwhelm and Inadequacy"`

---

### 2. SUMMARY
```javascript
// Access the data
const summary = response.summary;

// Basic stats
summary.week_period       // "2025-01-12 to 2025-01-18"
summary.entry_count       // 7
summary.overall_mood      // "negative"
summary.sentiment_score   // -0.42

// Patterns (array of objects)
summary.key_patterns.forEach(p => {
  console.log(p.pattern);      // "Feelings of Overwhelm"
  console.log(p.severity);     // "moderate"
  console.log(p.description);  // Full description
});

// Topics (simple array)
summary.main_topics  // ["work_stress", "anxiety", "panic_attacks"]
```

---

### 3. SUGGESTIONS
```javascript
// Just an array of strings
response.suggestions.forEach(suggestion => {
  console.log(suggestion);
  // "Explore boundary-setting skills"
  // "Discuss social anxiety patterns"
  // etc.
});
```

---

## API Endpoint

### POST to either of these:

**Option 1:** `/api/analyze-week`
```bash
POST http://localhost:5001/api/analyze-week
Content-Type: application/json

{
  "week_start": "2025-01-12",
  "week_end": "2025-01-18"
}
```

**Option 2:** `/api/process-full-pipeline` (recommended)
```bash
POST http://localhost:5001/api/process-full-pipeline
Content-Type: application/json

{
  "doc_urls": [
    {"url": "Journal text...", "date": "2025-01-12"},
    {"url": "Journal text...", "date": "2025-01-13"}
  ],
  "week_start": "2025-01-12",
  "week_end": "2025-01-18"
}
```

**Both return the same 3-section format!**

---

## Quick Test

### Using curl:
```bash
curl -X POST http://localhost:5001/api/process-full-pipeline \
  -H "Content-Type: application/json" \
  -d '{
    "doc_urls": [
      {"url": "I felt overwhelmed today", "date": "2025-01-12"}
    ],
    "week_start": "2025-01-12",
    "week_end": "2025-01-18"
  }'
```

### Using JavaScript fetch:
```javascript
const response = await fetch('http://localhost:5001/api/process-full-pipeline', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    doc_urls: [
      {url: "I felt overwhelmed today", date: "2025-01-12"}
    ],
    week_start: "2025-01-12",
    week_end: "2025-01-18"
  })
});

const data = await response.json();

console.log('Theme:', data.theme);
console.log('Mood:', data.summary.overall_mood);
console.log('Suggestions:', data.suggestions.length);
```

### Using Python:
```python
import requests

response = requests.post('http://localhost:5001/api/process-full-pipeline', json={
    "doc_urls": [
        {"url": "I felt overwhelmed today", "date": "2025-01-12"}
    ],
    "week_start": "2025-01-12",
    "week_end": "2025-01-18"
})

data = response.json()
print(f"Theme: {data['theme']}")
print(f"Mood: {data['summary']['overall_mood']}")
print(f"Patterns: {len(data['summary']['key_patterns'])}")
print(f"Suggestions: {len(data['suggestions'])}")
```

---

## Display Example (React)

```jsx
function WeeklyReport({ data }) {
  return (
    <div className="report">
      {/* 1. Theme */}
      <h1 className="theme">{data.theme}</h1>

      {/* 2. Summary */}
      <div className="summary">
        <div className="stats">
          <span>Week: {data.summary.week_period}</span>
          <span>Entries: {data.summary.entry_count}</span>
          <span>Mood: {data.summary.overall_mood}</span>
          <span>Score: {data.summary.sentiment_score}</span>
        </div>

        <div className="patterns">
          <h2>Key Patterns</h2>
          {data.summary.key_patterns.map((p, i) => (
            <div key={i} className={`pattern ${p.severity}`}>
              <strong>{p.pattern}</strong>
              <span className="badge">{p.severity}</span>
              <p>{p.description}</p>
            </div>
          ))}
        </div>

        <div className="topics">
          {data.summary.main_topics.map((topic, i) => (
            <span key={i} className="tag">{topic}</span>
          ))}
        </div>
      </div>

      {/* 3. Suggestions */}
      <div className="suggestions">
        <h2>Action Items</h2>
        <ul>
          {data.suggestions.map((s, i) => (
            <li key={i}>{s}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
```

---

## That's It!

**3 sections. Super simple:**

1. **`theme`** → String (main pattern)
2. **`summary`** → Object (week data)
3. **`suggestions`** → Array (action items)

See `API_RESPONSE_FORMAT.md` for more detailed examples and styling tips!
