"""
DEMO SCRIPT: Show the Value of Therapist Copilot

This script demonstrates:
1. Weekly analysis for immediate insights
2. Month-long trend analysis showing progression
3. Before/after comparison proving therapy effectiveness

Perfect for showcasing to stakeholders!
"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5001"

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def print_section(title):
    """Print section divider"""
    print(f"\n{'─'*70}")
    print(f"  {title}")
    print(f"{'─'*70}\n")

def demo_step1_weekly_analysis():
    """STEP 1: Analyze Week 1 (Baseline - High Anxiety)"""
    print_header("STEP 1: WEEKLY ANALYSIS - Week 1 (Baseline)")
    print("📅 Analyzing: January 6-12, 2025 (First week of therapy)")
    print("⏳ Running ChatGPT analysis...\n")

    response = requests.post(f"{BASE_URL}/api/analyze-week", json={
        "week_start": "2025-01-06",
        "week_end": "2025-01-12"
    })

    if response.status_code == 200:
        result = response.json()
        summary = result['summary']

        print(f"🎯 THEME: {result['theme']}\n")

        if 'patterns' in summary:
            print(f"🔍 KEY PATTERNS IDENTIFIED:")
            for i, pattern in enumerate(summary['patterns'][:3], 1):
                print(f"\n  {i}. {pattern.get('title', 'N/A')}")
                print(f"     • Severity: {pattern.get('severity', 'N/A').upper()}")
                print(f"     • Type: {pattern.get('type', 'N/A')}")
                desc = pattern.get('description', '')[:120]
                print(f"     • {desc}...")

        if 'mood_trends' in summary:
            mood = summary['mood_trends']
            print(f"\n💭 MOOD ASSESSMENT:")
            print(f"   • Overall: {mood.get('overall_sentiment', 'N/A').upper()}")
            print(f"   • Sentiment Score: {mood.get('sentiment_score', 'N/A')}")
            print(f"   • Trend: {mood.get('mood_shift', 'N/A')}")

        if 'clinical_prompts' in summary:
            print(f"\n💡 THERAPIST ACTION ITEMS:")
            for i, prompt in enumerate(summary['clinical_prompts'][:3], 1):
                print(f"   {i}. {prompt}")

        print("\n✅ Week 1 Analysis Complete")
        return result
    else:
        print(f"❌ Error: {response.text}")
        return None

def demo_step2_weekly_progress():
    """STEP 2: Show Week 4 for comparison"""
    print_header("STEP 2: WEEKLY ANALYSIS - Week 4 (Progress Check)")
    print("📅 Analyzing: January 27 - February 2, 2025 (4 weeks into therapy)")
    print("⏳ Running ChatGPT analysis...\n")

    response = requests.post(f"{BASE_URL}/api/analyze-week", json={
        "week_start": "2025-01-27",
        "week_end": "2025-02-02"
    })

    if response.status_code == 200:
        result = response.json()
        summary = result['summary']

        print(f"🎯 THEME: {result['theme']}\n")

        if 'patterns' in summary:
            print(f"🔍 KEY PATTERNS IDENTIFIED:")
            for i, pattern in enumerate(summary['patterns'][:3], 1):
                print(f"\n  {i}. {pattern.get('title', 'N/A')}")
                print(f"     • Severity: {pattern.get('severity', 'N/A').upper()}")
                desc = pattern.get('description', '')[:120]
                print(f"     • {desc}...")

        if 'mood_trends' in summary:
            mood = summary['mood_trends']
            print(f"\n💭 MOOD ASSESSMENT:")
            print(f"   • Overall: {mood.get('overall_sentiment', 'N/A').upper()}")
            print(f"   • Sentiment Score: {mood.get('sentiment_score', 'N/A')}")

        if 'strengths_observed' in summary:
            print(f"\n✨ STRENGTHS IDENTIFIED:")
            for strength in summary['strengths_observed'][:3]:
                print(f"   • {strength}")

        print("\n✅ Week 4 Analysis Complete")
        return result
    else:
        print(f"❌ Error: {response.text}")
        return None

def demo_step3_longterm_analysis():
    """STEP 3: Month-long trend analysis"""
    print_header("STEP 3: LONG-TERM TREND ANALYSIS (4 Weeks)")
    print("📅 Analyzing: Full month (January 6 - February 2, 2025)")
    print("🔬 Identifying meta-patterns across all 4 weeks...")
    print("⏳ This may take 10-15 seconds...\n")

    response = requests.post(f"{BASE_URL}/api/analyze-long-term", json={
        "start_date": "2025-01-06",
        "end_date": "2025-02-02"
    })

    if response.status_code == 200:
        result = response.json()
        analysis = result['analysis']

        print(f"📊 ANALYSIS PERIOD: {analysis.get('analysis_period', 'N/A')}")
        print(f"📈 WEEKS ANALYZED: {analysis.get('weeks_analyzed', 0)}\n")

        if 'trajectory' in analysis:
            traj = analysis['trajectory']
            print(f"📈 EMOTIONAL TRAJECTORY:")
            print(f"   • Direction: {traj.get('overall_direction', 'N/A').upper()}")
            print(f"   • {traj.get('narrative', 'N/A')}")

        if 'meta_patterns' in analysis:
            print(f"\n🎯 META-PATTERNS (Cross-Week Themes):")
            for i, pattern in enumerate(analysis['meta_patterns'][:3], 1):
                print(f"\n   {i}. {pattern.get('theme', 'N/A')}")
                print(f"      • Trend: {pattern.get('severity_trend', 'N/A')}")
                print(f"      • Weeks Present: {len(pattern.get('weeks_present', []))}")
                print(f"      • {pattern.get('description', '')[:100]}...")

        if 'progress_indicators' in analysis:
            print(f"\n✅ PROGRESS INDICATORS:")
            for indicator in analysis['progress_indicators'][:4]:
                print(f"   • {indicator}")

        if 'treatment_recommendations' in analysis:
            print(f"\n💊 TREATMENT RECOMMENDATIONS:")
            for i, rec in enumerate(analysis['treatment_recommendations'][:3], 1):
                print(f"\n   {i}. {rec.get('approach', 'N/A')} (Priority: {rec.get('priority', 'N/A').upper()})")
                print(f"      Rationale: {rec.get('rationale', 'N/A')}")

        print("\n✅ Long-term Analysis Complete")
        return result
    else:
        print(f"❌ Error: {response.text}")
        return None

def demo_step4_value_summary():
    """STEP 4: Summary of value proposition"""
    print_header("VALUE PROPOSITION SUMMARY")

    print("🎯 WHAT THERAPIST COPILOT PROVIDES:\n")

    print("1️⃣  WEEKLY INSIGHTS (Immediate Value)")
    print("   • Real-time pattern detection from journal entries")
    print("   • Specific clinical prompts for next session")
    print("   • Mood tracking with quantified scores")
    print("   • Patient strengths identification")
    print("   ⏱️  Saves 30-45 minutes of pre-session prep time\n")

    print("2️⃣  MONTH-LONG TRENDS (Long-term Value)")
    print("   • Identify persistent vs. improving issues")
    print("   • Track therapy effectiveness objectively")
    print("   • Detect cyclical patterns (seasonal, weekly, etc.)")
    print("   • Evidence-based treatment adjustments")
    print("   📊 What took months to notice now visible in minutes\n")

    print("3️⃣  CLINICAL BENEFITS:")
    print("   • Data-driven insights complement clinical judgment")
    print("   • Earlier detection of concerning patterns")
    print("   • Quantifiable progress to share with patients")
    print("   • Reduced therapist burnout from manual tracking\n")

    print("4️⃣  PATIENT BENEFITS:")
    print("   • Therapist more prepared for sessions")
    print("   • Concrete evidence of progress during hard times")
    print("   • Validation that their effort is working")
    print("   • More targeted, effective therapy\n")

    print("💰 COST: ~$0.01-0.03 per week of analysis")
    print("⏱️  TIME SAVED: 30-45 min/week for therapist")
    print("📈 ROI: Immeasurable in better patient outcomes\n")

def main():
    """Run the full demo"""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + " "*18 + "THERAPIST COPILOT DEMO" + " "*28 + "█")
    print("█" + " "*12 + "AI-Powered Journal Analysis for Therapists" + " "*15 + "█")
    print("█" + " "*68 + "█")
    print("█"*70)

    print("\n📋 This demo will show:")
    print("   1. Weekly analysis of baseline anxiety (Week 1)")
    print("   2. Weekly analysis after 4 weeks of therapy")
    print("   3. Month-long trend showing measurable improvement")
    print("   4. Value proposition summary")

    input("\n▶️  Press ENTER to start the demo...")

    # Step 1: Week 1 Baseline
    week1_result = demo_step1_weekly_analysis()
    if week1_result:
        input("\n▶️  Press ENTER to continue to Week 4...")

    # Step 2: Week 4 Progress
    week4_result = demo_step2_weekly_progress()
    if week4_result:
        input("\n▶️  Press ENTER to see long-term trends...")

    # Step 3: Long-term analysis
    longterm_result = demo_step3_longterm_analysis()
    if longterm_result:
        input("\n▶️  Press ENTER for value summary...")

    # Step 4: Value summary
    demo_step4_value_summary()

    print_header("DEMO COMPLETE")
    print("📁 All analysis files saved to: data/")
    print("📊 View detailed JSON files for full insights")
    print("\n💡 TIP: Use these results to create visualizations for stakeholders!")
    print("\n🚀 Ready to deploy? See DEPLOYMENT_GUIDE.md for instructions\n")

if __name__ == "__main__":
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ Error: Flask server not responding properly")
            print("Please start the server first: python app.py")
            exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to Flask server")
        print("Please start the server first:")
        print("  cd backend")
        print("  python app.py")
        exit(1)

    main()
