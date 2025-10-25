from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
from datetime import datetime

from utils.google_doc_converter import convert_google_doc_to_json
from utils.analyzer import analyze_weekly_entries
from utils.long_term_analyzer import analyze_long_term_trends, compare_time_periods

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
BASE_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

def get_patient_data_dir(patient_id):
    """Get or create data directory for a specific patient"""
    patient_dir = os.path.join(BASE_DATA_DIR, patient_id)
    os.makedirs(patient_dir, exist_ok=True)
    return patient_dir

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Therapist Copilot Backend API is running"
    }), 200

@app.route('/api/convert-google-doc', methods=['POST'])
def convert_google_doc():
    """
    Convert Google Doc entries to JSON format

    Expected payload:
    {
        "patient_id": "patient_123",  # Required for multi-user
        "doc_url": "https://docs.google.com/document/d/...",
        "date": "2025-01-12"  # Optional, will extract from content if not provided
    }
    """
    try:
        data = request.json
        patient_id = data.get('patient_id', 'default')
        doc_url = data.get('doc_url')
        entry_date = data.get('date')

        if not doc_url:
            return jsonify({"error": "doc_url is required"}), 400

        # Get patient-specific directory
        patient_dir = get_patient_data_dir(patient_id)

        # Convert Google Doc to JSON entry
        entry = convert_google_doc_to_json(doc_url, entry_date)

        # Save as daily JSON file
        filename = f"{entry['date']}.json"
        filepath = os.path.join(patient_dir, filename)

        with open(filepath, 'w') as f:
            json.dump(entry, f, indent=2)

        return jsonify({
            "success": True,
            "message": "Entry converted and saved",
            "entry": entry,
            "file": filename
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/aggregate-week', methods=['POST'])
def aggregate_week():
    """
    Aggregate daily entries into a weekly file

    Expected payload:
    {
        "patient_id": "patient_123",  # Required for multi-user
        "week_start": "2025-01-12",
        "week_end": "2025-01-18"
    }
    """
    try:
        data = request.json
        patient_id = data.get('patient_id', 'default')
        week_start = data.get('week_start')
        week_end = data.get('week_end')

        if not week_start or not week_end:
            return jsonify({"error": "week_start and week_end are required"}), 400

        # Get patient-specific directory
        patient_dir = get_patient_data_dir(patient_id)

        # Find all daily JSON files in the date range
        from datetime import datetime, timedelta
        start_date = datetime.strptime(week_start, '%Y-%m-%d')
        end_date = datetime.strptime(week_end, '%Y-%m-%d')

        entries = []
        current_date = start_date

        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            filepath = os.path.join(patient_dir, f"{date_str}.json")

            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    entry = json.load(f)
                    entries.append(entry)

            current_date += timedelta(days=1)

        # Create weekly aggregated file
        weekly_data = {
            "patient_id": patient_id,
            "week_start": week_start,
            "week_end": week_end,
            "entries": entries
        }

        weekly_filename = f"week_{week_start}_to_{week_end}.json"
        weekly_filepath = os.path.join(patient_dir, weekly_filename)

        with open(weekly_filepath, 'w') as f:
            json.dump(weekly_data, f, indent=2)

        return jsonify({
            "success": True,
            "message": "Weekly entries aggregated",
            "entry_count": len(entries),
            "file": weekly_filename,
            "weekly_data": weekly_data
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze-week', methods=['POST'])
def analyze_week():
    """
    Analyze weekly entries using ChatGPT and send results to frontend

    Expected payload:
    {
        "patient_id": "patient_123",  # Required for multi-user
        "week_start": "2025-01-12",
        "week_end": "2025-01-18"
    }
    """
    try:
        data = request.json
        patient_id = data.get('patient_id', 'default')
        week_start = data.get('week_start')
        week_end = data.get('week_end')

        if not week_start or not week_end:
            return jsonify({"error": "week_start and week_end are required"}), 400

        # Get patient-specific directory
        patient_dir = get_patient_data_dir(patient_id)
        week_file = f"week_{week_start}_to_{week_end}.json"

        # Load weekly data
        weekly_filepath = os.path.join(patient_dir, week_file)

        if not os.path.exists(weekly_filepath):
            return jsonify({"error": f"Weekly file not found: {week_file}"}), 404

        with open(weekly_filepath, 'r') as f:
            weekly_data = json.load(f)

        # Analyze using ChatGPT
        analysis = analyze_weekly_entries(weekly_data)

        # Save analysis summary
        summary_filename = f"summary_{weekly_data['week_start']}_to_{weekly_data['week_end']}.json"
        summary_filepath = os.path.join(patient_dir, summary_filename)

        with open(summary_filepath, 'w') as f:
            json.dump(analysis, f, indent=2)

        # Build simple summary text
        mood_trends = analysis.get('mood_trends', {})
        patterns = analysis.get('patterns', [])

        summary_text = f"Week of {weekly_data['week_start']} to {weekly_data['week_end']}. "
        summary_text += f"Analyzed {len(weekly_data.get('entries', []))} journal entries. "
        summary_text += f"Overall mood: {mood_trends.get('overall_sentiment', 'neutral')} "
        summary_text += f"(score: {mood_trends.get('sentiment_score', 0):.2f}). "

        if patterns:
            summary_text += f"Primary concerns: {', '.join([p.get('title', '') for p in patterns[:3]])}."

        # Simple 3-section response
        response_data = {
            "theme": analysis.get('patterns', [])[0].get('title', 'Weekly Insights') if analysis.get('patterns') else 'Weekly Insights',
            "summary": summary_text,
            "plan": analysis.get('clinical_prompts', [])
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/process-full-pipeline', methods=['POST'])
def process_full_pipeline():
    """
    Full pipeline: Convert docs, aggregate week, analyze, and return results

    Expected payload:
    {
        "patient_id": "patient_123",  # Required for multi-user
        "doc_urls": [
            {"url": "https://docs.google.com/...", "date": "2025-01-12"},
            {"url": "https://docs.google.com/...", "date": "2025-01-13"}
        ],
        "week_start": "2025-01-12",
        "week_end": "2025-01-18"
    }
    """
    try:
        data = request.json
        patient_id = data.get('patient_id', 'default')
        doc_urls = data.get('doc_urls', [])
        week_start = data.get('week_start')
        week_end = data.get('week_end')

        # Get patient-specific directory
        patient_dir = get_patient_data_dir(patient_id)

        results = {
            "converted_entries": [],
            "aggregation": None,
            "analysis": None
        }

        # Step 1: Convert all Google Docs
        for doc_data in doc_urls:
            entry = convert_google_doc_to_json(doc_data['url'], doc_data.get('date'))
            filename = f"{entry['date']}.json"
            filepath = os.path.join(patient_dir, filename)

            with open(filepath, 'w') as f:
                json.dump(entry, f, indent=2)

            results['converted_entries'].append(entry)

        # Step 2: Aggregate into weekly file
        from datetime import datetime, timedelta
        start_date = datetime.strptime(week_start, '%Y-%m-%d')
        end_date = datetime.strptime(week_end, '%Y-%m-%d')

        entries = []
        current_date = start_date

        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            filepath = os.path.join(patient_dir, f"{date_str}.json")

            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    entry = json.load(f)
                    entries.append(entry)

            current_date += timedelta(days=1)

        weekly_data = {
            "patient_id": patient_id,
            "week_start": week_start,
            "week_end": week_end,
            "entries": entries
        }

        weekly_filename = f"week_{week_start}_to_{week_end}.json"
        weekly_filepath = os.path.join(patient_dir, weekly_filename)

        with open(weekly_filepath, 'w') as f:
            json.dump(weekly_data, f, indent=2)

        results['aggregation'] = {
            "entry_count": len(entries),
            "file": weekly_filename
        }

        # Step 3: Analyze
        analysis = analyze_weekly_entries(weekly_data)

        summary_filename = f"summary_{week_start}_to_{week_end}.json"
        summary_filepath = os.path.join(patient_dir, summary_filename)

        with open(summary_filepath, 'w') as f:
            json.dump(analysis, f, indent=2)

        # Build simple summary text
        mood_trends = analysis.get('mood_trends', {})
        patterns = analysis.get('patterns', [])

        summary_text = f"Week of {week_start} to {week_end}. "
        summary_text += f"Analyzed {len(entries)} journal entries. "
        summary_text += f"Overall mood: {mood_trends.get('overall_sentiment', 'neutral')} "
        summary_text += f"(score: {mood_trends.get('sentiment_score', 0):.2f}). "

        if patterns:
            summary_text += f"Primary concerns: {', '.join([p.get('title', '') for p in patterns[:3]])}."

        # Simple 3-section response
        response_data = {
            "theme": analysis.get('patterns', [])[0].get('title', 'Weekly Insights') if analysis.get('patterns') else 'Weekly Insights',
            "summary": summary_text,
            "plan": analysis.get('clinical_prompts', [])
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze-long-term', methods=['POST'])
def analyze_long_term():
    """
    Analyze trends over a longer period (month, year, etc.)

    Expected payload:
    {
        "start_date": "2025-01-01",
        "end_date": "2025-03-31"
    }
    """
    try:
        data = request.json
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if not start_date or not end_date:
            return jsonify({"error": "start_date and end_date are required"}), 400

        # Perform long-term analysis
        analysis = analyze_long_term_trends(start_date, end_date, DATA_DIR)

        # Save long-term analysis
        filename = f"long_term_analysis_{start_date}_to_{end_date}.json"
        filepath = os.path.join(DATA_DIR, filename)

        with open(filepath, 'w') as f:
            json.dump(analysis, f, indent=2)

        return jsonify({
            "success": True,
            "analysis": analysis,
            "file": filename
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/compare-periods', methods=['POST'])
def compare_periods():
    """
    Compare two time periods

    Expected payload:
    {
        "period1": {"start": "2025-01-01", "end": "2025-01-31"},
        "period2": {"start": "2025-02-01", "end": "2025-02-28"}
    }
    """
    try:
        data = request.json
        period1 = data.get('period1')
        period2 = data.get('period2')

        if not period1 or not period2:
            return jsonify({"error": "period1 and period2 are required"}), 400

        # Compare the two periods
        comparison = compare_time_periods(
            period1['start'], period1['end'],
            period2['start'], period2['end'],
            DATA_DIR
        )

        # Save comparison
        filename = f"comparison_{period1['start']}_vs_{period2['start']}.json"
        filepath = os.path.join(DATA_DIR, filename)

        with open(filepath, 'w') as f:
            json.dump(comparison, f, indent=2)

        return jsonify({
            "success": True,
            "comparison": comparison,
            "file": filename
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/patients', methods=['GET'])
def list_patients():
    """
    List all patients with data in the system
    """
    try:
        os.makedirs(BASE_DATA_DIR, exist_ok=True)
        patients = [d for d in os.listdir(BASE_DATA_DIR)
                   if os.path.isdir(os.path.join(BASE_DATA_DIR, d)) and not d.startswith('.')]

        # Get entry counts for each patient
        patient_info = []
        for patient_id in patients:
            patient_dir = os.path.join(BASE_DATA_DIR, patient_id)
            files = [f for f in os.listdir(patient_dir) if f.endswith('.json') and not f.startswith('week_') and not f.startswith('summary_')]
            patient_info.append({
                "patient_id": patient_id,
                "entry_count": len(files)
            })

        return jsonify({"patients": patient_info}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Ensure base data directory exists
    os.makedirs(BASE_DATA_DIR, exist_ok=True)

    # Run the app
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
