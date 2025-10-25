"""
Generate AI analyses for all new patients
"""
import requests
import json

BASE_URL = "http://localhost:5050"

def analyze_patient_week(patient_id, week_start, week_end):
    """Analyze a patient's week"""
    print(f"\n🤖 Analyzing {patient_id} ({week_start} to {week_end})...")

    try:
        response = requests.post(
            f"{BASE_URL}/api/analyze-week",
            json={
                "patient_id": patient_id,
                "week_start": week_start,
                "week_end": week_end
            }
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success!")
            print(f"   Theme: {result.get('theme', 'N/A')}")
            print(f"   {result.get('summary', 'N/A')[:100]}...")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return False

    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def main():
    print("="*70)
    print("  GENERATING AI ANALYSES FOR NEW PATIENTS")
    print("="*70)

    # Check if OpenAI key is configured
    print("\n⚠️  Note: This requires OPENAI_API_KEY in .env file")
    print("   If not configured, analyses will fail.\n")

    # Analyze James Rivera
    analyze_patient_week("james-rivera", "2025-02-10", "2025-02-16")

    # Analyze Alex Kim
    analyze_patient_week("alex-kim", "2025-02-10", "2025-02-16")

    print("\n" + "="*70)
    print("✅ DONE!")
    print("="*70)
    print("\nCheck http://localhost:3000 to see all patients!")

if __name__ == "__main__":
    main()
