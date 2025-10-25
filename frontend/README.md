# Therapist Copilot Frontend

Vite + React dashboard that visualizes insights from the Flask backend in `../backend`. The UI now loads real data via REST so you can demo the full pipeline end to end.

## Getting Started

1. Install dependencies (Node 18+ recommended):
   ```bash
   npm install
   ```
2. Copy the example environment file and adjust the API URL if needed:
   ```bash
   cp .env.example .env
   # set VITE_API_BASE_URL to wherever the Flask app is running
   ```
3. Start the dev server:
   ```bash
   npm run dev
   ```
4. Run the Flask backend from `../backend/app.py` so the dashboard can fetch data.

## API Contract

The frontend expects the backend to expose:
- `GET /api/patients` – returns `{ patients: [{ patient_id, name, entry_count, latest_week }] }`
- `GET /api/patients/<patient_id>/analyses` – returns `{ analyses: WeeklyAnalysis[] }` where each analysis contains the `summary`, `patterns`, and `clinical_prompts` displayed in the UI.

Update `VITE_API_BASE_URL` if you deploy the backend somewhere other than `http://localhost:5000`.
