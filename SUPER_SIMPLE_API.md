# Super Simple API - Just 3 Things!

## What You Get Back

```json
{
  "theme": "One-line main pattern",
  "summary": "Text paragraph summarizing the week",
  "plan": ["Action item 1", "Action item 2", "Action item 3"]
}
```

That's it! No nested objects, no complex structure. Just 3 simple sections.

---

## Real Example

### Request:
```bash
POST http://localhost:5001/api/process-full-pipeline

{
  "doc_urls": [
    {"url": "I felt overwhelmed today...", "date": "2025-01-12"}
  ],
  "week_start": "2025-01-12",
  "week_end": "2025-01-18"
}
```

### Response:
```json
{
  "theme": "Feelings of Overwhelm and Inadequacy",

  "summary": "Week of 2025-01-12 to 2025-01-18. Analyzed 7 journal entries. Overall mood: negative (score: -0.42). Primary concerns: Feelings of Overwhelm and Inadequacy, Avoidance and Isolation, Coping with Panic and Anxiety.",

  "plan": [
    "Explore the patient's fear of setting boundaries and its impact on their well-being",
    "Discuss the patient's avoidance of social interactions and underlying fears of rejection",
    "Examine the patient's experiences with panic attacks and explore effective coping strategies",
    "Consider the patient's feelings of isolation and muted emotions",
    "Encourage the patient to identify positive experiences and moments of hope"
  ]
}
```

---

## How to Use It

### JavaScript:
```javascript
const response = await fetch('http://localhost:5001/api/process-full-pipeline', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    doc_urls: [{url: "Journal text...", date: "2025-01-12"}],
    week_start: "2025-01-12",
    week_end: "2025-01-18"
  })
});

const data = await response.json();

// Just 3 things:
console.log(data.theme);      // String
console.log(data.summary);    // String
console.log(data.plan);       // Array of strings
```

### Display It:
```jsx
function Report({ data }) {
  return (
    <div>
      <h1>{data.theme}</h1>
      <p>{data.summary}</p>
      <h2>Action Plan</h2>
      <ul>
        {data.plan.map((item, i) => (
          <li key={i}>{item}</li>
        ))}
      </ul>
    </div>
  );
}
```

---

## Python:
```python
import requests

response = requests.post('http://localhost:5001/api/process-full-pipeline', json={
    "doc_urls": [{"url": "Journal text...", "date": "2025-01-12"}],
    "week_start": "2025-01-12",
    "week_end": "2025-01-18"
})

data = response.json()

print("Theme:", data['theme'])
print("Summary:", data['summary'])
print("Plan items:", len(data['plan']))
```

---

## That's All!

Three fields:
1. **`theme`** → String (main pattern)
2. **`summary`** → String (week overview)
3. **`plan`** → Array (action items)

Super simple. No nesting. Easy to use.
