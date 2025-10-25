"""
Simple test script for Therapist Copilot Backend

Run this after starting the Flask server to test all endpoints.

Usage:
    python test_backend.py
"""
import requests
import json
import sys

BASE_URL = "http://localhost:5000"

def print_response(name, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print()

def test_health():
    """Test health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    return response.status_code == 200

def test_convert_entries():
    """Test converting multiple entries"""
    # Load test data
    with open('test_data.json', 'r') as f:
        test_data = json.load(f)

    entries = test_data['sample_entries'][:3]  # Test with first 3 entries

    print(f"\nConverting {len(entries)} test entries...")

    for entry in entries:
        response = requests.post(
            f"{BASE_URL}/api/convert-google-doc",
            json={
                "doc_url": entry["text"],
                "date": entry["date"]
            }
        )

        if response.status_code != 200:
            print_response(f"Convert Entry {entry['date']}", response)
            return False

    print("✓ All entries converted successfully")
    return True

def test_aggregate_week():
    """Test aggregating entries into weekly file"""
    response = requests.post(
        f"{BASE_URL}/api/aggregate-week",
        json={
            "week_start": "2025-01-12",
            "week_end": "2025-01-18"
        }
    )

    print_response("Aggregate Weekly Entries", response)
    return response.status_code == 200

def test_analyze_week():
    """Test ChatGPT analysis of weekly entries"""
    print("\n⚠️  This test requires a valid OPENAI_API_KEY in .env")
    print("It will make an API call to OpenAI (costs ~$0.01)")

    user_input = input("Continue with analysis test? (y/n): ")
    if user_input.lower() != 'y':
        print("Skipping analysis test")
        return True

    response = requests.post(
        f"{BASE_URL}/api/analyze-week",
        json={
            "week_start": "2025-01-12",
            "week_end": "2025-01-18"
        }
    )

    print_response("Analyze Weekly Entries", response)
    return response.status_code == 200

def test_full_pipeline():
    """Test the complete pipeline in one call"""
    # Load test data
    with open('test_data.json', 'r') as f:
        test_data = json.load(f)

    print("\n⚠️  This test requires a valid OPENAI_API_KEY in .env")
    print("It will make an API call to OpenAI (costs ~$0.01)")

    user_input = input("Continue with full pipeline test? (y/n): ")
    if user_input.lower() != 'y':
        print("Skipping full pipeline test")
        return True

    response = requests.post(
        f"{BASE_URL}/api/process-full-pipeline",
        json={
            "doc_urls": [
                {"url": entry["text"], "date": entry["date"]}
                for entry in test_data["sample_entries"]
            ],
            "week_start": "2025-01-12",
            "week_end": "2025-01-18"
        }
    )

    print_response("Full Pipeline", response)

    if response.status_code == 200:
        result = response.json()
        print("\n" + "="*60)
        print("ANALYSIS SUMMARY")
        print("="*60)
        print(f"Theme: {result['results']['analysis']['theme']}")
        print(f"\nPatterns Found: {len(result['results']['analysis']['summary'].get('patterns', []))}")
        print(f"Clinical Prompts: {len(result['results']['analysis']['summary'].get('clinical_prompts', []))}")
        print("\nTop Clinical Prompt:")
        prompts = result['results']['analysis']['summary'].get('clinical_prompts', [])
        if prompts:
            print(f"  • {prompts[0]}")

    return response.status_code == 200

def main():
    """Run all tests"""
    print("="*60)
    print("THERAPIST COPILOT - BACKEND API TESTS")
    print("="*60)
    print(f"\nTesting server at: {BASE_URL}")
    print("Make sure the Flask server is running (python app.py)\n")

    tests = [
        ("Health Check", test_health),
        ("Convert Entries", test_convert_entries),
        ("Aggregate Week", test_aggregate_week),
        ("Analyze Week", test_analyze_week),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except requests.exceptions.ConnectionError:
            print(f"\n❌ ERROR: Cannot connect to {BASE_URL}")
            print("Make sure the Flask server is running:")
            print("  python app.py")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ ERROR in {name}: {str(e)}")
            results.append((name, False))

    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")

    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"\nPassed: {passed}/{total}")

    # Optional: Full pipeline test
    print("\n" + "="*60)
    print("OPTIONAL: Full Pipeline Test")
    print("="*60)
    test_full_pipeline()

if __name__ == "__main__":
    main()
