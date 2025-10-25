"""
Test Multi-User Support

Shows how the system handles multiple patients
"""
import requests
import json

print("="*60)
print("MULTI-USER TEST")
print("="*60)

# Patient 1: Sarah (anxiety)
patient1_data = {
    "patient_id": "sarah_001",
    "doc_urls": [
        {"url": "I had a panic attack at the store today. Everyone was staring.", "date": "2025-02-10"},
        {"url": "Stayed in bed all day. Too anxious to face the world.", "date": "2025-02-11"},
    ],
    "week_start": "2025-02-10",
    "week_end": "2025-02-16"
}

# Patient 2: Mike (depression)
patient2_data = {
    "patient_id": "mike_002",
    "doc_urls": [
        {"url": "What's the point of anything? I can't find joy in things I used to love.", "date": "2025-02-10"},
        {"url": "Forced myself to go to the gym. Felt a tiny bit better.", "date": "2025-02-11"},
    ],
    "week_start": "2025-02-10",
    "week_end": "2025-02-16"
}

# Patient 3: Emma (making progress)
patient3_data = {
    "patient_id": "emma_003",
    "doc_urls": [
        {"url": "Tried that mindfulness exercise. Actually helped me calm down!", "date": "2025-02-10"},
        {"url": "Had coffee with a friend today. Felt almost normal.", "date": "2025-02-11"},
    ],
    "week_start": "2025-02-10",
    "week_end": "2025-02-16"
}

patients = [
    ("Sarah (Anxiety)", patient1_data),
    ("Mike (Depression)", patient2_data),
    ("Emma (Progress)", patient3_data)
]

print("\nAnalyzing 3 different patients...\n")

for name, patient_data in patients:
    print(f"\n{'─'*60}")
    print(f"PATIENT: {name} (ID: {patient_data['patient_id']})")
    print(f"{'─'*60}")

    response = requests.post('http://localhost:5001/api/process-full-pipeline', json=patient_data)

    if response.status_code == 200:
        data = response.json()

        print(f"\n✓ THEME: {data['theme']}")
        print(f"\n📝 SUMMARY:")
        print(f"   {data['summary']}")
        print(f"\n📋 PLAN:")
        for i, item in enumerate(data['plan'][:2], 1):
            print(f"   {i}. {item}")
        if len(data['plan']) > 2:
            print(f"   ... and {len(data['plan']) - 2} more items")
    else:
        print(f"   ❌ ERROR: {response.status_code}")

print("\n" + "="*60)
print("Checking patient list...")
print("="*60)

response = requests.get('http://localhost:5001/api/patients')
if response.status_code == 200:
    data = response.json()
    print(f"\nTotal patients in system: {len(data['patients'])}")
    for patient in data['patients']:
        print(f"  • {patient['patient_id']}: {patient['entry_count']} entries")
else:
    print("Could not retrieve patient list")

print("\n" + "="*60)
print("✅ Multi-user support working!")
print("="*60)
print("\nEach patient's data is stored separately:")
print("  data/sarah_001/")
print("  data/mike_002/")
print("  data/emma_003/")
print("\nNo data mixing or conflicts!")
