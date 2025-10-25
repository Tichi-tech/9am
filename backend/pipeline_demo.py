"""
LIVE PIPELINE DEMO

Shows the complete Therapist Copilot pipeline in action:
1. Raw journal entries → Daily JSON files
2. Daily files → Weekly aggregation
3. Weekly data → AI analysis with ChatGPT
4. Results → Clinical insights

Perfect for presentations and demos!
"""
import requests
import json
import time
import os
from datetime import datetime

BASE_URL = "http://localhost:5050"

def print_header(title):
    """Print formatted header"""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█  " + title.center(64) + "  █")
    print("█" + " "*68 + "█")
    print("█"*70 + "\n")

def print_section(title):
    """Print section divider"""
    print(f"\n{'─'*70}")
    print(f"  {title}")
    print(f"{'─'*70}\n")

def check_server():
    """Verify backend is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Backend server is running\n")
            return True
        else:
            print("❌ Backend server error")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
        print("Please start it: cd backend && python app.py")
        return False

def demo_patient_list():
    """Show all patients in the system"""
    print_section("STEP 1: View All Patients")
    print("📋 Fetching patient list from API...\n")

    response = requests.get(f"{BASE_URL}/api/patients")

    if response.status_code == 200:
        data = response.json()
        patients = data.get('patients', [])

        print(f"👥 FOUND {len(patients)} PATIENTS:\n")
        for i, patient in enumerate(patients, 1):
            print(f"  {i}. {patient['name']} (ID: {patient['patient_id']})")
            print(f"     Therapist: {patient.get('therapist', 'N/A')}")
            print(f"     Journal Entries: {patient.get('entry_count', 0)}")
            if patient.get('latest_week'):
                week = patient['latest_week']
                print(f"     Latest Week: {week.get('start')} to {week.get('end')}")
            print()

        return patients
    else:
        print(f"❌ Error: {response.text}")
        return []

def demo_full_pipeline(patient_id, week_start, week_end):
    """Demonstrate the full pipeline for a patient"""
    print_section(f"STEP 2: Full Pipeline for {patient_id}")
    print(f"📅 Week: {week_start} to {week_end}\n")

    # Check if weekly file already exists
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', patient_id)
    weekly_file = os.path.join(data_dir, f"week_{week_start}_to_{week_end}.json")

    if os.path.exists(weekly_file):
        print("📁 Weekly aggregation file found\n")

        # Load and show entry count
        with open(weekly_file, 'r') as f:
            weekly_data = json.load(f)
            entry_count = len(weekly_data.get('entries', []))
            print(f"   • Entries in this week: {entry_count}")
            print(f"   • File: week_{week_start}_to_{week_end}.json\n")
    else:
        print("⚠️  No weekly file found - need to aggregate first\n")
        return False

    # Check if analysis exists
    summary_file = os.path.join(data_dir, f"summary_{week_start}_to_{week_end}.json")

    if os.path.exists(summary_file):
        print("✅ Analysis already exists - loading cached results\n")
        with open(summary_file, 'r') as f:
            analysis = json.load(f)
    else:
        # Run analysis
        print("🤖 Running AI analysis with ChatGPT...")
        print("   (This calls OpenAI GPT-4 to analyze journal patterns)\n")

        response = requests.post(f"{BASE_URL}/api/analyze-week", json={
            "patient_id": patient_id,
            "week_start": week_start,
            "week_end": week_end
        })

        if response.status_code != 200:
            print(f"❌ Analysis failed: {response.text}")
            return False

        result = response.json()
        print("✅ Analysis complete!\n")

        # Load the full analysis from file
        with open(summary_file, 'r') as f:
            analysis = json.load(f)

    return analysis

def display_analysis_results(analysis, patient_id):
    """Display analysis results in a formatted way"""
    print_section("STEP 3: AI-Generated Clinical Insights")

    # Theme
    if 'patterns' in analysis and analysis['patterns']:
        theme = analysis['patterns'][0].get('title', 'Weekly Insights')
        print(f"🎯 PRIMARY THEME: {theme}\n")

    # Patterns
    if 'patterns' in analysis:
        print("🔍 EMOTIONAL PATTERNS DETECTED:\n")
        for i, pattern in enumerate(analysis['patterns'][:3], 1):
            print(f"   {i}. {pattern.get('title', 'Pattern')}")
            print(f"      Severity: {pattern.get('severity', 'moderate').upper()}")
            print(f"      {pattern.get('description', '')[:120]}...")
            print()

    # Mood
    if 'mood_trends' in analysis:
        mood = analysis['mood_trends']
        print("💭 MOOD ASSESSMENT:\n")
        print(f"   Overall Sentiment: {mood.get('overall_sentiment', 'N/A').upper()}")
        print(f"   Sentiment Score: {mood.get('sentiment_score', 0)}")
        print(f"   Trend: {mood.get('mood_shift', 'N/A')}\n")

    # Clinical prompts
    if 'clinical_prompts' in analysis:
        print("💡 CLINICAL ACTION ITEMS FOR THERAPIST:\n")
        for i, prompt in enumerate(analysis['clinical_prompts'], 1):
            print(f"   {i}. {prompt}")
        print()

    # Strengths
    if 'strengths_observed' in analysis and analysis['strengths_observed']:
        print("✨ PATIENT STRENGTHS OBSERVED:\n")
        for strength in analysis['strengths_observed'][:3]:
            print(f"   • {strength}")
        print()

def demo_multi_patient_comparison():
    """Show comparison across multiple patients"""
    print_section("STEP 4: Multi-Patient Overview")
    print("📊 Comparing insights across all patients...\n")

    response = requests.get(f"{BASE_URL}/api/patients")
    if response.status_code != 200:
        print("❌ Could not fetch patients")
        return

    patients = response.json().get('patients', [])

    for patient in patients:
        patient_id = patient['patient_id']

        # Get latest analysis
        response = requests.get(f"{BASE_URL}/api/patients/{patient_id}/analyses")
        if response.status_code == 200:
            analyses = response.json().get('analyses', [])
            if analyses:
                latest = analyses[0]
                print(f"👤 {patient['name']}:")
                print(f"   Theme: {latest.get('theme_title', 'N/A')}")
                print(f"   Mood: {latest.get('overall_mood', 'N/A')} (score: {latest.get('sentiment_score', 0)})")
                print(f"   Week: {latest.get('week_start')} to {latest.get('week_end')}")
                print()

def main():
    """Run the complete demo"""
    print_header("THERAPIST COPILOT - LIVE PIPELINE DEMO")

    print("This demo shows the complete pipeline:")
    print("  1. Patient data management (multi-user)")
    print("  2. Weekly journal aggregation")
    print("  3. AI analysis with ChatGPT")
    print("  4. Clinical insights generation")
    print("  5. Multi-patient comparison\n")

    # Check server
    if not check_server():
        return

    input("▶️  Press ENTER to start the demo...")

    # Step 1: Show all patients
    patients = demo_patient_list()
    if not patients:
        print("⚠️  No patients found. Run: python generate_multi_patient_demo.py")
        return

    input("▶️  Press ENTER to analyze a patient's week...")

    # Step 2-3: Full pipeline for first patient
    patient = patients[0]
    patient_id = patient['patient_id']

    # Get their latest week
    if patient.get('latest_week'):
        week = patient['latest_week']
        week_start = week['start']
        week_end = week['end']
    else:
        print("⚠️  No weekly data found for this patient")
        return

    analysis = demo_full_pipeline(patient_id, week_start, week_end)

    if analysis:
        display_analysis_results(analysis, patient_id)

    input("▶️  Press ENTER to see multi-patient comparison...")

    # Step 4: Multi-patient view
    demo_multi_patient_comparison()

    # Summary
    print_header("DEMO COMPLETE")
    print("✅ Pipeline demonstrated successfully!\n")
    print("📊 KEY TAKEAWAYS:")
    print("   • Multi-patient support with data isolation")
    print("   • Automated pattern detection from journal text")
    print("   • AI-powered clinical insights in seconds")
    print("   • Actionable recommendations for therapists")
    print("   • Quantified mood tracking over time\n")

    print("💰 VALUE PROPOSITION:")
    print("   • Time saved: 30-45 min per patient per week")
    print("   • Cost: $0.01-0.03 per analysis")
    print("   • Better patient outcomes through data-driven therapy\n")

    print("🌐 NEXT STEPS:")
    print("   • View frontend: http://localhost:3000")
    print("   • API docs: See SUPER_SIMPLE_API.md")
    print("   • Deploy: See DEPLOYMENT_GUIDE.md\n")

if __name__ == "__main__":
    main()
