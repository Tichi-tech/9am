"""
Multi-Patient Demo Data Generator

Creates realistic data for 3 diverse patients to showcase:
1. Different therapeutic scenarios
2. Multi-user capabilities
3. Variety of emotional patterns
"""
import json
import os
from datetime import datetime, timedelta

def create_patient_registry():
    """Create patients.json with 3 diverse patients"""
    patients = {
        "patients": [
            {
                "id": "maya-thompson",
                "name": "Maya Thompson",
                "therapist": "Dr. Evelyn Carter",
                "timezone": "America/Los_Angeles",
                "scenario": "Workplace anxiety and social isolation - showing improvement"
            },
            {
                "id": "james-rivera",
                "name": "James Rivera",
                "therapist": "Dr. Sarah Chen",
                "timezone": "America/New_York",
                "scenario": "Grief counseling after loss of partner - processing emotions"
            },
            {
                "id": "alex-kim",
                "name": "Alex Kim",
                "therapist": "Dr. Michael Torres",
                "timezone": "America/Chicago",
                "scenario": "Career burnout and perfectionism - learning boundaries"
            }
        ]
    }
    return patients

def generate_james_entries():
    """Patient 2: Grief counseling - processing loss"""
    return [
        {
            "date": "2025-02-10",
            "time": "23:45",
            "text": "Three months since David passed. The house is too quiet. I found his coffee mug in the cabinet today and just sat on the kitchen floor and cried for an hour."
        },
        {
            "date": "2025-02-11",
            "time": "06:30",
            "text": "Woke up and reached for him again. The grief comes in waves. Sometimes I'm okay and then something small - a song, a smell - and I'm drowning again."
        },
        {
            "date": "2025-02-12",
            "time": "19:00",
            "text": "Friends invited me to dinner. Made up an excuse. I know they're trying to help but I can't pretend to be okay right now. The therapy sessions help more than social obligations."
        },
        {
            "date": "2025-02-13",
            "time": "14:30",
            "text": "Went through some of David's things today. Found letters he wrote me when we were dating. Laughed and cried at the same time. Grief is so confusing - joy and pain all mixed together."
        },
        {
            "date": "2025-02-14",
            "time": "21:00",
            "text": "Valentine's Day. Our day. Instead of falling apart, I went to our favorite restaurant and had dinner alone. Toasted to his memory. It hurt but it also felt right. He'd want me to remember the good."
        },
        {
            "date": "2025-02-15",
            "time": "10:00",
            "text": "Therapy today. Talked about how grief isn't linear. Some days I'm okay, some days I'm not. Learning that both are acceptable. David wouldn't want me stuck in sadness forever."
        },
        {
            "date": "2025-02-16",
            "time": "16:45",
            "text": "Decided to donate some of David's clothes. Kept his favorite sweater and watch. Baby steps. It's not about forgetting him, it's about learning to live with the loss."
        }
    ]

def generate_alex_entries():
    """Patient 3: Career burnout and perfectionism"""
    return [
        {
            "date": "2025-02-10",
            "time": "22:30",
            "text": "Stayed at the office until 10pm again. Everyone else left at 6. My manager didn't even ask me to stay late - I just can't leave work undone. Why am I like this?"
        },
        {
            "date": "2025-02-11",
            "time": "07:00",
            "text": "Checking emails before I even get out of bed. Already anxious about today's presentation. Spent 6 hours on slides that took everyone else 2. It's still not perfect. It's never perfect."
        },
        {
            "date": "2025-02-12",
            "time": "20:00",
            "text": "Presentation went fine. Got good feedback. So why do I feel like a failure? Keep replaying the one question I fumbled. Nobody else probably even noticed. My brain is exhausting."
        },
        {
            "date": "2025-02-13",
            "time": "15:30",
            "text": "Therapy session was tough. Talked about how my self-worth is tied to productivity. Therapist asked 'what would happen if you weren't perfect?' Honestly? It terrifies me."
        },
        {
            "date": "2025-02-14",
            "time": "18:00",
            "text": "Tried the homework - left work at 5:30pm. Felt guilty the entire evening. Keep thinking about the emails I didn't answer. This is supposed to get easier, right?"
        },
        {
            "date": "2025-02-15",
            "time": "12:00",
            "text": "Said 'no' to taking on an extra project. First time ever. My manager was fine with it. Why did I think the world would end if I set a boundary?"
        },
        {
            "date": "2025-02-16",
            "time": "21:30",
            "text": "Weird realization: I've been running from something my whole life. Not towards success, but away from feeling 'not good enough.' Therapy is showing me I've been fighting the wrong battle."
        }
    ]

def save_patient_data(patient_id, entries, week_start, week_end):
    """Save patient data in their isolated directory"""
    # Create patient directory
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    patient_dir = os.path.join(base_dir, patient_id)
    os.makedirs(patient_dir, exist_ok=True)

    # Save daily files
    for entry in entries:
        filename = f"{entry['date']}.json"
        filepath = os.path.join(patient_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(entry, f, indent=2)

    # Save weekly aggregate
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

    print(f"✓ Saved {len(entries)} entries for {patient_id}")
    return patient_dir

def main():
    """Generate multi-patient demo data"""
    print("\n" + "="*70)
    print("  MULTI-PATIENT DEMO DATA GENERATOR")
    print("="*70 + "\n")

    # 1. Create patient registry
    print("📋 Creating patient registry...")
    registry = create_patient_registry()
    registry_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'patients.json')
    with open(registry_path, 'w') as f:
        json.dump(registry, f, indent=2)
    print(f"✓ Registry saved: {registry_path}\n")

    # 2. Generate data for James (Grief counseling)
    print("👤 Generating data for James Rivera (Grief Counseling)...")
    james_entries = generate_james_entries()
    save_patient_data("james-rivera", james_entries, "2025-02-10", "2025-02-16")

    # 3. Generate data for Alex (Career burnout)
    print("👤 Generating data for Alex Kim (Career Burnout)...")
    alex_entries = generate_alex_entries()
    save_patient_data("alex-kim", alex_entries, "2025-02-10", "2025-02-16")

    print("\n" + "="*70)
    print("✅ MULTI-PATIENT DEMO DATA GENERATED SUCCESSFULLY!")
    print("="*70 + "\n")

    print("📊 PATIENT OVERVIEW:\n")
    for patient in registry['patients']:
        print(f"  • {patient['name']} ({patient['id']})")
        print(f"    Therapist: {patient['therapist']}")
        print(f"    Scenario: {patient['scenario']}\n")

    print("📁 Data Location: data/")
    print("   • data/maya-thompson/   (Anxiety - existing data)")
    print("   • data/james-rivera/    (Grief - 7 entries)")
    print("   • data/alex-kim/        (Burnout - 7 entries)")

    print("\n🚀 NEXT STEPS:")
    print("   1. Backend server will auto-detect new patients")
    print("   2. Run: python pipeline_demo.py  (to see full pipeline)")
    print("   3. Check frontend at http://localhost:3000")
    print("   4. API: http://localhost:5050/api/patients\n")

if __name__ == "__main__":
    main()
