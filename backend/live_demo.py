"""
LIVE INTERACTIVE DEMO - Therapist Copilot

Perfect for showing stakeholders how the system works!
This script:
1. Shows you a raw journal entry
2. Processes it through the pipeline in real-time
3. Displays the AI-generated insights
4. Shows before/after comparison

Run this when demoing to non-technical people!
"""
import requests
import json
import time
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5050"

# Sample journal entries you can use in demos
DEMO_JOURNAL_ENTRIES = {
    "anxiety": """
Today was rough. Had a panic attack during the team meeting. My heart was racing
and I felt like everyone was staring at me. I had to step out. Again.

I'm so tired of feeling like this. My therapist says I'm making progress but I
don't see it. Keep canceling plans with friends because I'm too anxious to leave
the house. Mom called and I didn't pick up. What would I even say?

Tried that breathing exercise tonight. It helped a little, I guess. But I still
feel like I'm drowning most of the time.
""",

    "depression": """
Woke up at 2pm. Couldn't find a reason to get out of bed earlier. Everything
feels heavy and pointless. Scrolled on my phone for hours but nothing made me
feel anything.

Jake texted asking if I wanted to grab coffee. Said I was busy. I wasn't. I just
can't fake being okay right now. He probably thinks I hate him. I don't. I hate me.

Therapist tomorrow. Part of me wants to cancel. What's the point of talking about
the same things over and over? But I promised myself I'd try. One day at a time,
or whatever they say.
""",

    "improvement": """
Actually had a good day today. Is that allowed? Went for a walk this morning and
the sun felt nice. Weird how I'm almost suspicious of feeling okay.

Made it through the work presentation without panicking. Used those breathing
techniques my therapist taught me. They actually worked! People even said I did
well. Old me wouldn't believe this is possible.

Called Mom back. We talked for 20 minutes and it was nice. I told her about therapy
and she was supportive. Why did I think she wouldn't understand?

Still anxious but it doesn't control me like it used to. Progress is real.
"""
}

def print_header(title, char="="):
    """Print a fancy header"""
    print("\n" + char*80)
    print(f"  {title}")
    print(char*80 + "\n")

def print_step(step_num, title):
    """Print a step header"""
    print(f"\n{'━'*80}")
    print(f"  STEP {step_num}: {title}")
    print(f"{'━'*80}\n")

def check_server():
    """Verify backend is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Backend server connected\n")
            return True
        else:
            print("❌ Backend server error")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
        print("\nPlease start it first:")
        print("  cd backend")
        print("  python app.py\n")
        return False

def show_menu():
    """Show journal entry options"""
    print("📝 Choose a demo journal entry:\n")
    print("  1. Anxiety/Panic (struggling)")
    print("  2. Depression/Low Mood (difficult week)")
    print("  3. Progress/Improvement (therapy working)")
    print("  4. Enter custom text")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == "1":
        return "anxiety", DEMO_JOURNAL_ENTRIES["anxiety"]
    elif choice == "2":
        return "depression", DEMO_JOURNAL_ENTRIES["depression"]
    elif choice == "3":
        return "improvement", DEMO_JOURNAL_ENTRIES["improvement"]
    elif choice == "4":
        print("\nEnter journal text (press Ctrl+D or Ctrl+Z when done):")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass
        return "custom", "\n".join(lines)
    else:
        return "anxiety", DEMO_JOURNAL_ENTRIES["anxiety"]

def display_journal(text, scenario):
    """Display the raw journal entry"""
    print_step(1, "RAW JOURNAL ENTRY")

    print(f"📖 Scenario: {scenario.title()}")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d')}")
    print("\n" + "─"*80)
    print(text.strip())
    print("─"*80 + "\n")

def create_demo_week(entry_text, patient_id="demo-patient"):
    """Create a week of entries with this as the latest"""
    print_step(2, "CREATING WEEKLY DATA")
    print("📦 Packaging journal entries for AI analysis...")

    # Use dates from this week
    today = datetime.now()
    week_start = (today - timedelta(days=6)).strftime('%Y-%m-%d')
    week_end = today.strftime('%Y-%m-%d')

    # Create a week of entries (we'll just use one for demo)
    entry = {
        "date": today.strftime('%Y-%m-%d'),
        "time": datetime.now().strftime('%H:%M'),
        "text": entry_text
    }

    # Create weekly data structure
    weekly_data = {
        "patient_id": patient_id,
        "week_start": week_start,
        "week_end": week_end,
        "entries": [entry]
    }

    print(f"✅ Week range: {week_start} to {week_end}")
    print(f"✅ Entries prepared: 1 entry")
    print(f"✅ Patient ID: {patient_id}\n")

    return weekly_data, week_start, week_end

def analyze_with_ai(weekly_data, patient_id, week_start, week_end):
    """Send to AI for analysis"""
    print_step(3, "AI ANALYSIS")
    print("🤖 Sending to ChatGPT for pattern analysis...")
    print("⏳ This takes 3-5 seconds...\n")

    # Save the weekly file first
    import os
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    patient_dir = os.path.join(base_dir, patient_id)
    os.makedirs(patient_dir, exist_ok=True)

    # Save daily entry
    entry = weekly_data['entries'][0]
    daily_path = os.path.join(patient_dir, f"{entry['date']}.json")
    with open(daily_path, 'w') as f:
        json.dump(entry, f, indent=2)

    # Save weekly aggregate
    weekly_path = os.path.join(patient_dir, f"week_{week_start}_to_{week_end}.json")
    with open(weekly_path, 'w') as f:
        json.dump(weekly_data, f, indent=2)

    # Analyze
    start_time = time.time()

    try:
        response = requests.post(
            f"{BASE_URL}/api/analyze-week",
            json={
                "patient_id": patient_id,
                "week_start": week_start,
                "week_end": week_end
            },
            timeout=30
        )

        elapsed = time.time() - start_time

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Analysis complete in {elapsed:.1f} seconds!\n")
            return result
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}\n")
            return None

    except Exception as e:
        print(f"❌ Exception: {str(e)}\n")
        return None

def display_results(result):
    """Display the AI analysis results"""
    print_step(4, "AI-GENERATED INSIGHTS")

    # Main theme
    theme = result.get('theme', 'N/A')
    print(f"🎯 PRIMARY THEME DETECTED:\n")
    print(f"   → {theme}")

    # Summary
    summary = result.get('summary', '')
    if summary:
        print(f"\n📊 SUMMARY:\n")
        print(f"   {summary}")

    # Clinical plan
    plan = result.get('plan', [])
    if plan:
        print(f"\n💡 CLINICAL ACTION ITEMS FOR THERAPIST:\n")
        for i, item in enumerate(plan, 1):
            print(f"   {i}. {item}")

    print()

def show_value_prop():
    """Show the value proposition"""
    print_step(5, "VALUE DELIVERED")

    print("⏱️  TIME COMPARISON:\n")
    print("   Traditional approach:")
    print("   • Therapist reads journal: 15-20 min")
    print("   • Identifies patterns: 10-15 min")
    print("   • Prepares session notes: 10-15 min")
    print("   • TOTAL: 30-45 minutes per patient\n")

    print("   With Therapist Copilot:")
    print("   • AI analysis: 3-5 seconds")
    print("   • Therapist reviews insights: 3-5 min")
    print("   • TOTAL: 5 minutes per patient\n")

    print("   ✨ TIME SAVED: 25-40 minutes (85-90% reduction)\n")

    print("💰 COST:\n")
    print("   • AI analysis: $0.01-0.03 per entry")
    print("   • Therapist time saved: $40-60 (at $100/hr rate)")
    print("   • ROI: 2,000x - 4,000x\n")

    print("🎯 CLINICAL BENEFITS:\n")
    print("   • Patterns detected therapist might miss")
    print("   • Objective mood tracking")
    print("   • Specific session prompts")
    print("   • Patient strengths identified")
    print("   • Better prepared sessions = better outcomes\n")

def demo_full_analysis():
    """Run a full analysis demo"""
    print_header("THERAPIST COPILOT - LIVE DEMO", "█")

    print("This demo shows the complete pipeline:")
    print("  1. Raw journal entry (what patient writes)")
    print("  2. Data processing (automatic)")
    print("  3. AI analysis with ChatGPT (the magic)")
    print("  4. Clinical insights (what therapist gets)")
    print("  5. Value delivered (time & quality)\n")

    # Check server
    if not check_server():
        return

    # Select journal entry
    scenario, journal_text = show_menu()

    input("\n▶️  Press ENTER to start the analysis...")

    # Step 1: Show raw journal
    display_journal(journal_text, scenario)

    input("▶️  Press ENTER to process this entry...")

    # Step 2: Create weekly data
    weekly_data, week_start, week_end = create_demo_week(journal_text)

    input("▶️  Press ENTER to send to AI for analysis...")

    # Step 3: AI Analysis
    result = analyze_with_ai(weekly_data, "demo-patient", week_start, week_end)

    if not result:
        print("⚠️  Analysis failed. Check that OPENAI_API_KEY is configured.\n")
        return

    input("▶️  Press ENTER to see the results...")

    # Step 4: Display results
    display_results(result)

    input("▶️  Press ENTER to see the value proposition...")

    # Step 5: Value prop
    show_value_prop()

    # Done!
    print_header("DEMO COMPLETE", "█")
    print("🎉 You just saw:")
    print("   • Raw journal → AI insights in seconds")
    print("   • Emotional patterns automatically detected")
    print("   • Specific clinical recommendations generated")
    print("   • 25-40 minutes saved per patient\n")

    print("🌐 Next Steps:")
    print("   • Try the frontend: http://localhost:3000")
    print("   • View all patients: python pipeline_demo.py")
    print("   • See API docs: ../SUPER_SIMPLE_API.md\n")

    again = input("Run another demo? (y/n): ").strip().lower()
    if again == 'y':
        demo_full_analysis()

if __name__ == "__main__":
    demo_full_analysis()
