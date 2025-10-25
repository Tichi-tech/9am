# Multi-User Support Guide

## Overview

The system now supports **multiple patients**! Each patient's data is completely isolated in separate folders.

---

## How It Works

### Data Organization:
```
data/
├── patient_001/
│   ├── 2025-02-01.json
│   ├── 2025-02-02.json
│   ├── week_2025-02-01_to_2025-02-07.json
│   └── summary_2025-02-01_to_2025-02-07.json
│
├── patient_002/
│   ├── 2025-02-01.json
│   ├── 2025-02-02.json
│   └── week_2025-02-01_to_2025-02-07.json
│
└── patient_003/
    ├── 2025-02-01.json
    └── ...
```

**Each patient gets their own folder!**

---

## Using Multi-User API

### Just Add `patient_id` to Your Requests

**Before (single user):**
```json
{
  "doc_urls": [...],
  "week_start": "2025-02-01",
  "week_end": "2025-02-07"
}
```

**After (multi-user):**
```json
{
  "patient_id": "patient_123",
  "doc_urls": [...],
  "week_start": "2025-02-01",
  "week_end": "2025-02-07"
}
```

**That's it!** Just one extra field.

---

## Examples

### Example 1: Sarah (Anxiety Patient)
```javascript
fetch('http://localhost:5001/api/process-full-pipeline', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    patient_id: "sarah_001",
    doc_urls: [
      {url: "Had a panic attack today...", date: "2025-02-10"}
    ],
    week_start: "2025-02-10",
    week_end: "2025-02-16"
  })
});
```

**Response:**
```json
{
  "theme": "Panic and Social Anxiety",
  "summary": "Week of 2025-02-10 to 2025-02-16. Analyzed 1 journal entries...",
  "plan": ["Explore panic triggers...", "Develop coping strategies..."]
}
```

**Files created:**
- `data/sarah_001/2025-02-10.json`
- `data/sarah_001/week_2025-02-10_to_2025-02-16.json`
- `data/sarah_001/summary_2025-02-10_to_2025-02-16.json`

---

### Example 2: Mike (Depression Patient)
```javascript
fetch('http://localhost:5001/api/process-full-pipeline', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    patient_id: "mike_002",
    doc_urls: [
      {url: "Can't find joy in anything...", date: "2025-02-10"}
    ],
    week_start: "2025-02-10",
    week_end: "2025-02-16"
  })
});
```

**Files created:**
- `data/mike_002/2025-02-10.json`
- `data/mike_002/week_2025-02-10_to_2025-02-16.json`
- `data/mike_002/summary_2025-02-10_to_2025-02-16.json`

**Sarah's data and Mike's data are completely separate!**

---

## List All Patients

**New Endpoint:**
```bash
GET /api/patients
```

**Response:**
```json
{
  "patients": [
    {"patient_id": "sarah_001", "entry_count": 5},
    {"patient_id": "mike_002", "entry_count": 3},
    {"patient_id": "emma_003", "entry_count": 7}
  ]
}
```

---

## Frontend Integration

### Simple Patient Selector:
```javascript
// Get list of patients
async function loadPatients() {
  const response = await fetch('http://localhost:5001/api/patients');
  const data = await response.json();
  return data.patients;
}

// Get analysis for specific patient
async function getPatientAnalysis(patientId, weekStart, weekEnd) {
  const response = await fetch('http://localhost:5001/api/process-full-pipeline', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      patient_id: patientId,
      doc_urls: [...],  // Patient's entries
      week_start: weekStart,
      week_end: weekEnd
    })
  });

  return await response.json();
}

// Usage
const patients = await loadPatients();
const sarahAnalysis = await getPatientAnalysis('sarah_001', '2025-02-10', '2025-02-16');
```

---

## React Example

```jsx
function TherapistDashboard() {
  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [analysis, setAnalysis] = useState(null);

  // Load patient list on mount
  useEffect(() => {
    fetch('http://localhost:5001/api/patients')
      .then(res => res.json())
      .then(data => setPatients(data.patients));
  }, []);

  // Load analysis when patient selected
  const loadPatientData = async (patientId) => {
    const response = await fetch('http://localhost:5001/api/process-full-pipeline', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        patient_id: patientId,
        doc_urls: [...],
        week_start: '2025-02-10',
        week_end: '2025-02-16'
      })
    });

    const data = await response.json();
    setAnalysis(data);
  };

  return (
    <div>
      {/* Patient selector */}
      <select onChange={(e) => loadPatientData(e.target.value)}>
        {patients.map(p => (
          <option key={p.patient_id} value={p.patient_id}>
            {p.patient_id} ({p.entry_count} entries)
          </option>
        ))}
      </select>

      {/* Show analysis */}
      {analysis && (
        <div>
          <h1>{analysis.theme}</h1>
          <p>{analysis.summary}</p>
          <ul>
            {analysis.plan.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
```

---

## API Changes Summary

### All Endpoints Now Accept `patient_id`:

1. **POST /api/convert-google-doc**
   - Add: `"patient_id": "patient_123"`

2. **POST /api/aggregate-week**
   - Add: `"patient_id": "patient_123"`

3. **POST /api/analyze-week**
   - Add: `"patient_id": "patient_123"`

4. **POST /api/process-full-pipeline**
   - Add: `"patient_id": "patient_123"`

5. **NEW: GET /api/patients**
   - Returns list of all patients

---

## Default Behavior

**If you don't provide `patient_id`, it uses `"default"`:**

```javascript
// This works (uses "default" patient)
fetch('/api/process-full-pipeline', {
  method: 'POST',
  body: JSON.stringify({
    doc_urls: [...],
    week_start: "2025-02-10",
    week_end: "2025-02-16"
  })
});

// Files saved to: data/default/
```

**Backward compatible!** Old code still works.

---

## Best Practices

### Patient IDs:
- Use consistent format: `patient_001`, `patient_002`
- Or use anonymized IDs: `anon_a1b2c3`
- Or use UUIDs: `550e8400-e29b-41d4-a716-446655440000`

### Data Isolation:
✅ Each patient's data is in separate folder
✅ No risk of data mixing
✅ Easy to delete patient data (just remove folder)
✅ Easy to export patient data (just zip folder)

---

## Testing

### Run Multi-User Test:
```bash
cd backend
python test_multi_user.py
```

This creates 3 test patients and verifies data isolation.

---

## Production Considerations

For production, you'll want to:

1. **Authentication**: Map user sessions to patient_ids
2. **Authorization**: Ensure therapists only access their patients
3. **Database**: Consider moving to PostgreSQL for better multi-user support
4. **Encryption**: Encrypt patient_id in transit and at rest

---

## Summary

**Multi-user support is now active!**

- ✅ Just add `patient_id` to requests
- ✅ Data stored in separate folders
- ✅ New `/api/patients` endpoint
- ✅ Backward compatible
- ✅ Ready for frontend integration

**Your friend can now build a patient selector UI!** 🎉
