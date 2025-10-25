# Test Output Example - Simple API

## Actual Response from API

Here's what you get back when you POST to the API:

```json
{
  "theme": "Overwhelm and Boundaries",

  "summary": "Week of 2025-01-12 to 2025-01-18. Analyzed 7 journal entries. Overall mood: mixed (score: -0.20). Primary concerns: Overwhelm and Boundaries, Isolation and Fear of Rejection, Coping with Panic and Anxiety.",

  "plan": [
    "Explore the patient's fear of rejection and its impact on relationships.",
    "Discuss the patient's experience with panic attacks and potential coping strategies.",
    "Examine the patient's difficulty with setting boundaries and its relation to work stress.",
    "Consider the patient's perception of normalcy and how it affects their mood.",
    "Address the patient's feelings of guilt and how they relate to family dynamics."
  ]
}
```

---

## Console Output

```
Testing full pipeline with ChatGPT analysis...
This will use your OpenAI API key and cost ~$0.01

✓ SUCCESS!

============================================================
ANALYSIS RESULTS - 3 SECTIONS
============================================================

1️⃣  THEME:
    Overwhelm and Boundaries

2️⃣  SUMMARY:
    Week of 2025-01-12 to 2025-01-18. Analyzed 7 journal entries.
    Overall mood: mixed (score: -0.20). Primary concerns: Overwhelm
    and Boundaries, Isolation and Fear of Rejection, Coping with
    Panic and Anxiety.

3️⃣  PLAN (5):
    1. Explore the patient's fear of rejection and its impact on relationships.
    2. Discuss the patient's experience with panic attacks and potential coping strategies.
    3. Examine the patient's difficulty with setting boundaries and its relation to work stress.
    4. Consider the patient's perception of normalcy and how it affects their mood.
    5. Address the patient's feelings of guilt and how they relate to family dynamics.

============================================================
```

---

## What Each Field Contains

### `theme` (string)
**One-line summary of the main pattern**

Examples:
- `"Overwhelm and Boundaries"`
- `"Social Anxiety and Avoidance"`
- `"Building Resilience and Hope"`

---

### `summary` (string)
**Text paragraph with key information**

Format:
```
Week of {start} to {end}. Analyzed {N} journal entries.
Overall mood: {mood} (score: {-1.0 to 1.0}).
Primary concerns: {top 3 patterns}.
```

Example:
```
Week of 2025-01-12 to 2025-01-18. Analyzed 7 journal entries.
Overall mood: mixed (score: -0.20). Primary concerns: Overwhelm
and Boundaries, Isolation and Fear of Rejection, Coping with
Panic and Anxiety.
```

---

### `plan` (array of strings)
**5-7 action items for the therapist**

Each item is a specific, actionable clinical prompt:
```json
[
  "Explore the patient's fear of rejection",
  "Discuss panic attacks and coping strategies",
  "Examine difficulty with setting boundaries"
]
```

---

## How to Display This

### Simple HTML:
```html
<div class="analysis-report">
  <h1 class="theme">Overwhelm and Boundaries</h1>

  <p class="summary">
    Week of 2025-01-12 to 2025-01-18. Analyzed 7 journal entries.
    Overall mood: mixed (score: -0.20). Primary concerns: Overwhelm
    and Boundaries, Isolation and Fear of Rejection, Coping with
    Panic and Anxiety.
  </p>

  <div class="plan">
    <h2>Action Plan</h2>
    <ol>
      <li>Explore the patient's fear of rejection and its impact on relationships.</li>
      <li>Discuss the patient's experience with panic attacks and potential coping strategies.</li>
      <li>Examine the patient's difficulty with setting boundaries and its relation to work stress.</li>
      <li>Consider the patient's perception of normalcy and how it affects their mood.</li>
      <li>Address the patient's feelings of guilt and how they relate to family dynamics.</li>
    </ol>
  </div>
</div>
```

### React:
```jsx
function WeeklyReport({ data }) {
  return (
    <div className="analysis-report">
      <h1 className="theme">{data.theme}</h1>

      <p className="summary">{data.summary}</p>

      <div className="plan">
        <h2>Action Plan</h2>
        <ol>
          {data.plan.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ol>
      </div>
    </div>
  );
}
```

---

## Quick Copy-Paste Frontend Code

```javascript
// Fetch the analysis
async function getAnalysis() {
  const response = await fetch('http://localhost:5001/api/process-full-pipeline', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      doc_urls: [
        {url: "Journal entry text...", date: "2025-01-12"}
      ],
      week_start: "2025-01-12",
      week_end: "2025-01-18"
    })
  });

  const data = await response.json();

  // Use the 3 sections
  document.getElementById('theme').textContent = data.theme;
  document.getElementById('summary').textContent = data.summary;

  const planList = document.getElementById('plan');
  data.plan.forEach(item => {
    const li = document.createElement('li');
    li.textContent = item;
    planList.appendChild(li);
  });
}
```

---

## Testing It Yourself

1. **Start the backend:**
   ```bash
   cd backend
   python app.py
   ```

2. **Run the test:**
   ```bash
   python quick_test.py
   ```

3. **Or use curl:**
   ```bash
   curl -X POST http://localhost:5001/api/process-full-pipeline \
     -H "Content-Type: application/json" \
     -d '{
       "doc_urls": [{"url": "Test entry", "date": "2025-01-12"}],
       "week_start": "2025-01-12",
       "week_end": "2025-01-18"
     }' | python -m json.tool
   ```

---

## That's It!

Super simple. Just 3 fields. No complexity.

Copy the JSON, plug it into your frontend, and you're done! 🎉
