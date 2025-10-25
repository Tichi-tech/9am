"""
Test with completely new journal entries to verify pipeline works
"""
import requests
import json

print("Testing with BRAND NEW journal entries...")
print("="*60)

# Create 3 completely new entries
new_entries = [
    {
        "url": "Today was rough. I had a big presentation at work and I completely froze. My boss asked me a question and my mind went blank. I felt like everyone was judging me. Came home and cried for an hour.",
        "date": "2025-02-01"
    },
    {
        "url": "Didn't want to get out of bed this morning. What's the point? I keep messing everything up. My friend texted but I ignored it. I don't deserve their friendship anyway.",
        "date": "2025-02-02"
    },
    {
        "url": "Tried that breathing exercise my therapist taught me when I felt anxious today. It actually helped a little. Maybe there's hope? I don't know. Baby steps I guess.",
        "date": "2025-02-03"
    }
]

print(f"\nSending {len(new_entries)} new entries to pipeline...")
print("\nEntries:")
for i, entry in enumerate(new_entries, 1):
    print(f"  {i}. [{entry['date']}] {entry['url'][:60]}...")

response = requests.post('http://localhost:5001/api/process-full-pipeline', json={
    "doc_urls": new_entries,
    "week_start": "2025-02-01",
    "week_end": "2025-02-07"
})

print(f"\nResponse Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()

    print("\n" + "="*60)
    print("✓ SUCCESS! Pipeline works perfectly!")
    print("="*60)

    print(f"\n1️⃣  THEME:")
    print(f"    {data['theme']}")

    print(f"\n2️⃣  SUMMARY:")
    print(f"    {data['summary']}")

    print(f"\n3️⃣  PLAN ({len(data['plan'])} items):")
    for i, item in enumerate(data['plan'], 1):
        print(f"    {i}. {item}")

    print("\n" + "="*60)
    print("FULL JSON RESPONSE:")
    print("="*60)
    print(json.dumps(data, indent=2))

    print("\n✅ All 3 sections present and working!")

else:
    print(f"\n❌ ERROR: {response.status_code}")
    print(response.text)
