import requests
import json

# Test data
data = {
    "doc_urls": [
        {
            "url": "I felt really overwhelmed today at work. Everyone needed something from me and I couldn't say no. By the time I got home, I just wanted to disappear. I know I should set boundaries but I'm afraid people will think I'm not a team player.",
            "date": "2025-01-12"
        },
        {
            "url": "I wanted to reach out to Sarah but didn't. I convinced myself she's probably busy and doesn't want to hear from me anyway. Why do I always do this? I push people away before they can leave me.",
            "date": "2025-01-13"
        },
        {
            "url": "Woke up feeling heavy again. This is the third day in a row. I used to love mornings. Now I just lie there thinking about all the ways I'm failing. Got up eventually and made coffee. Small victory, I guess.",
            "date": "2025-01-14"
        },
        {
            "url": "Had a panic attack before the meeting today. Heart racing, couldn't breathe. Locked myself in the bathroom for 10 minutes. No one noticed when I came back. Or if they did, they didn't say anything. I'm getting better at hiding it, which feels both good and terrible.",
            "date": "2025-01-15"
        },
        {
            "url": "Mom called. Didn't answer. She left a voicemail asking if I'm okay. I don't know how to explain that I'm not, and I'm also not sure I'm not. Everything feels muted, like I'm watching my life through frosted glass. Went for a walk instead. The cold air helped a little.",
            "date": "2025-01-16"
        },
        {
            "url": "Actually had a good conversation with my coworker Alex today. We talked about that new show everyone's watching. It felt normal. I realized I haven't felt normal in weeks. Made me sad but also gave me hope? Can't tell which emotion is winning.",
            "date": "2025-01-17"
        },
        {
            "url": "Therapy is tomorrow. I should make a list of things to talk about but everything feels both urgent and pointless at the same time. The panic attacks, the isolation, the work stress, the guilt about Mom. Where do I even start? Maybe I'll just see what comes up.",
            "date": "2025-01-18"
        }
    ],
    "week_start": "2025-01-12",
    "week_end": "2025-01-18"
}

print("Testing full pipeline with ChatGPT analysis...")
print("This will use your OpenAI API key and cost ~$0.01\n")

response = requests.post('http://localhost:5001/api/process-full-pipeline', json=data)

if response.status_code == 200:
    result = response.json()
    print("✓ SUCCESS!\n")
    print("="*60)
    print("ANALYSIS RESULTS - 3 SECTIONS")
    print("="*60)

    # Section 1: Theme
    print(f"\n1️⃣  THEME:")
    print(f"    {result['theme']}\n")

    # Section 2: Summary
    print(f"2️⃣  SUMMARY:")
    summary = result['summary']
    print(f"    Week: {summary.get('week_period', 'N/A')}")
    print(f"    Entries: {summary.get('entry_count', 0)}")
    print(f"    Overall Mood: {summary.get('overall_mood', 'N/A').upper()}")
    print(f"    Sentiment Score: {summary.get('sentiment_score', 0)}")

    # Patterns
    if 'key_patterns' in summary:
        print(f"\n    Key Patterns ({len(summary['key_patterns'])}):")
        for i, pattern in enumerate(summary['key_patterns'], 1):
            severity = pattern.get('severity', 'N/A').upper()
            print(f"\n      {i}. {pattern.get('pattern', 'N/A')} [{severity}]")
            desc = pattern.get('description', 'N/A')[:120]
            print(f"         {desc}...")

    # Topics
    if 'main_topics' in summary:
        topics = ', '.join(summary['main_topics'])
        print(f"\n    Main Topics: {topics}")

    # Section 3: Suggestions
    print(f"\n3️⃣  SUGGESTIONS ({len(result.get('suggestions', []))}):")
    for i, suggestion in enumerate(result.get('suggestions', []), 1):
        print(f"    {i}. {suggestion}")

    print("\n" + "="*60)
    print("\nFull response saved to: analysis_result.json")
    with open('analysis_result.json', 'w') as f:
        json.dump(result, f, indent=2)

else:
    print(f"❌ ERROR: {response.status_code}")
    print(response.text)
