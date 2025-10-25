# API Response Format - Simple 3-Section Structure

## Overview

All analysis endpoints return a **simple JSON object with exactly 3 sections**:

1. **`theme`** - Main pattern identified (string)
2. **`summary`** - Key information about the week (object)
3. **`suggestions`** - What the therapist should do (array of strings)

---

## Example Response

### POST `/api/analyze-week` or `/api/process-full-pipeline`

**Request:**
```json
{
  "week_start": "2025-01-12",
  "week_end": "2025-01-18"
}
```

**Response:**
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
        "pattern": "Feelings of Overwhelm and Inadequacy",
        "severity": "moderate",
        "description": "Patient frequently expresses feelings of being overwhelmed and inadequate, particularly in work settings. Multiple entries mention inability to say 'no' to others' requests."
      },
      {
        "pattern": "Avoidance and Isolation",
        "severity": "high",
        "description": "Patient exhibits pattern of avoiding social interactions due to fear of rejection. This avoidance seems to lead to feelings of loneliness and self-criticism."
      },
      {
        "pattern": "Coping with Panic and Anxiety",
        "severity": "moderate",
        "description": "Patient experiences panic attacks and uses avoidance as coping mechanism. Also mentions using walks as a way to manage stress."
      }
    ],
    "main_topics": [
      "work_stress",
      "social_anxiety",
      "panic_attacks",
      "family_relationships",
      "self_criticism"
    ]
  },

  "suggestions": [
    "Explore the patient's fear of setting boundaries and its impact on their well-being",
    "Discuss the patient's avoidance of social interactions and underlying fears of rejection",
    "Examine the patient's experiences with panic attacks and explore effective coping strategies",
    "Consider the patient's feelings of isolation and muted emotions",
    "Encourage the patient to identify positive experiences and moments of hope"
  ]
}
```

---

## Section Breakdown

### 1. `theme` (string)

**What it is:**
The primary pattern or issue identified across the week's entries.

**Examples:**
- `"Feelings of Overwhelm and Inadequacy"`
- `"Social Anxiety and Avoidance"`
- `"Building Coping Skills"`
- `"Progress with Self-Compassion"`

**How to use:**
Display this as the main headline or title for the week's analysis.

---

### 2. `summary` (object)

**What it is:**
Key metrics and patterns from the week.

**Fields:**

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `week_period` | string | Date range analyzed | `"2025-01-12 to 2025-01-18"` |
| `entry_count` | number | Number of journal entries | `7` |
| `overall_mood` | string | Overall sentiment | `"negative"`, `"neutral"`, `"positive"`, `"mixed"` |
| `sentiment_score` | number | Numeric mood score (-1 to +1) | `-0.42` |
| `key_patterns` | array | Top 3 patterns detected | See below |
| `main_topics` | array | Top 5 topics discussed | `["work_stress", "anxiety"]` |

**`key_patterns` structure:**
```json
{
  "pattern": "Name of the pattern",
  "severity": "low" | "moderate" | "high",
  "description": "Detailed explanation with evidence from entries"
}
```

**How to use:**
- Display mood score as a chart or gauge
- Show patterns as cards with color-coded severity
- List topics as tags or badges

---

### 3. `suggestions` (array of strings)

**What it is:**
Specific clinical prompts for the therapist to explore in the next session.

**Examples:**
```json
[
  "Explore the patient's fear of setting boundaries",
  "Discuss avoidance of social interactions",
  "Examine panic attack experiences and coping strategies",
  "Consider feelings of isolation and muted emotions",
  "Encourage identifying positive experiences"
]
```

**How to use:**
Display as a checklist or action items for the therapist.

---

## Frontend Display Example

### HTML Structure:
```html
<div class="analysis">
  <!-- Theme -->
  <h1 class="theme">{{ theme }}</h1>

  <!-- Summary -->
  <div class="summary">
    <div class="stat">
      <label>Week:</label>
      <span>{{ summary.week_period }}</span>
    </div>

    <div class="stat">
      <label>Mood:</label>
      <span>{{ summary.overall_mood }}</span>
      <span>{{ summary.sentiment_score }}</span>
    </div>

    <div class="patterns">
      <h2>Key Patterns</h2>
      {% for pattern in summary.key_patterns %}
      <div class="pattern severity-{{ pattern.severity }}">
        <h3>{{ pattern.pattern }}</h3>
        <p>{{ pattern.description }}</p>
      </div>
      {% endfor %}
    </div>

    <div class="topics">
      {% for topic in summary.main_topics %}
      <span class="tag">{{ topic }}</span>
      {% endfor %}
    </div>
  </div>

  <!-- Suggestions -->
  <div class="suggestions">
    <h2>Clinical Action Items</h2>
    <ul>
      {% for suggestion in suggestions %}
      <li>{{ suggestion }}</li>
      {% endfor %}
    </ul>
  </div>
</div>
```

### React Example:
```jsx
function AnalysisView({ data }) {
  return (
    <div className="analysis">
      {/* Theme */}
      <h1 className="theme">{data.theme}</h1>

      {/* Summary */}
      <div className="summary">
        <div className="stats">
          <div>Week: {data.summary.week_period}</div>
          <div>Entries: {data.summary.entry_count}</div>
          <div>Mood: {data.summary.overall_mood} ({data.summary.sentiment_score})</div>
        </div>

        <div className="patterns">
          <h2>Key Patterns</h2>
          {data.summary.key_patterns.map((pattern, i) => (
            <div key={i} className={`pattern severity-${pattern.severity}`}>
              <h3>{pattern.pattern}</h3>
              <p>{pattern.description}</p>
            </div>
          ))}
        </div>

        <div className="topics">
          {data.summary.main_topics.map((topic, i) => (
            <span key={i} className="tag">{topic}</span>
          ))}
        </div>
      </div>

      {/* Suggestions */}
      <div className="suggestions">
        <h2>Clinical Action Items</h2>
        <ul>
          {data.suggestions.map((suggestion, i) => (
            <li key={i}>{suggestion}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
```

---

## All Endpoints Using This Format

### 1. Analyze Weekly Entries
```bash
POST /api/analyze-week
{
  "week_start": "2025-01-12",
  "week_end": "2025-01-18"
}
```

### 2. Full Pipeline (Recommended)
```bash
POST /api/process-full-pipeline
{
  "doc_urls": [
    {"url": "Entry text...", "date": "2025-01-12"},
    {"url": "Entry text...", "date": "2025-01-13"}
  ],
  "week_start": "2025-01-12",
  "week_end": "2025-01-18"
}
```

**Both return the same 3-section format!**

---

## Severity Levels

Use these for color-coding patterns:

| Severity | Color | CSS Class | Meaning |
|----------|-------|-----------|---------|
| `low` | Green | `.severity-low` | Minor concern, manageable |
| `moderate` | Orange | `.severity-moderate` | Notable pattern, needs attention |
| `high` | Red | `.severity-high` | Significant concern, priority focus |

### Example CSS:
```css
.severity-low {
  background: #c6f6d5;
  color: #22543d;
  border-left: 4px solid #38a169;
}

.severity-moderate {
  background: #fed7aa;
  color: #7c2d12;
  border-left: 4px solid #f97316;
}

.severity-high {
  background: #feb2b2;
  color: #742a2a;
  border-left: 4px solid #dc2626;
}
```

---

## Sentiment Score Scale

| Score Range | Mood | Meaning |
|-------------|------|---------|
| +0.3 to +1.0 | Very Positive | High optimism, hope |
| +0.1 to +0.3 | Positive | Generally good mood |
| -0.1 to +0.1 | Neutral | Mixed or balanced |
| -0.3 to -0.1 | Negative | Generally low mood |
| -1.0 to -0.3 | Very Negative | High distress |

### Visual Display:
```javascript
function getSentimentColor(score) {
  if (score >= 0.3) return '#48bb78';      // Green
  if (score >= 0.1) return '#9ae6b4';      // Light green
  if (score >= -0.1) return '#ecc94b';     // Yellow
  if (score >= -0.3) return '#fc8181';     // Light red
  return '#f56565';                        // Red
}
```

---

## Testing the Response

### Using curl:
```bash
curl -X POST http://localhost:5001/api/process-full-pipeline \
  -H "Content-Type: application/json" \
  -d '{
    "doc_urls": [
      {"url": "I felt overwhelmed today...", "date": "2025-01-12"}
    ],
    "week_start": "2025-01-12",
    "week_end": "2025-01-18"
  }' | python -m json.tool
```

### Using Python:
```python
import requests

response = requests.post('http://localhost:5001/api/process-full-pipeline', json={
    "doc_urls": [
        {"url": "I felt overwhelmed today...", "date": "2025-01-12"}
    ],
    "week_start": "2025-01-12",
    "week_end": "2025-01-18"
})

data = response.json()
print(f"Theme: {data['theme']}")
print(f"Mood: {data['summary']['overall_mood']}")
print(f"Suggestions: {len(data['suggestions'])}")
```

### Using JavaScript (fetch):
```javascript
fetch('http://localhost:5001/api/process-full-pipeline', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    doc_urls: [
      {url: "I felt overwhelmed today...", date: "2025-01-12"}
    ],
    week_start: "2025-01-12",
    week_end: "2025-01-18"
  })
})
.then(res => res.json())
.then(data => {
  console.log('Theme:', data.theme);
  console.log('Mood:', data.summary.overall_mood);
  console.log('Patterns:', data.summary.key_patterns.length);
  console.log('Suggestions:', data.suggestions);
});
```

---

## Summary

**Your API returns exactly 3 things:**

1. **`theme`** - One-line main pattern (string)
2. **`summary`** - Week overview with mood, patterns, topics (object)
3. **`suggestions`** - Action items for therapist (array)

**That's it! Simple and clean.** ✨
