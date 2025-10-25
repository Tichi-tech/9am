"""
Weekly Journal Analyzer using OpenAI GPT-4

Analyzes weekly journal entries for emotional patterns, trends, and clinical insights
"""
import os
import json
from datetime import datetime
from openai import OpenAI

def load_prompt_template():
    """Load the analysis prompt template"""
    prompt_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'prompts',
        'analysis_prompt.txt'
    )

    with open(prompt_path, 'r') as f:
        return f.read()

def format_entries_for_analysis(weekly_data):
    """
    Format journal entries into readable text for GPT analysis

    Args:
        weekly_data: Dictionary containing week_start, week_end, and entries

    Returns:
        Formatted string of entries
    """
    entries_text = []

    for entry in weekly_data.get('entries', []):
        entry_text = f"""
Date: {entry.get('date', 'Unknown')}
Time: {entry.get('time', 'Unknown')}

{entry.get('text', '')}

---
"""
        entries_text.append(entry_text)

    return '\n'.join(entries_text)

def analyze_weekly_entries(weekly_data, model="gpt-4o", temperature=0.3):
    """
    Main function to analyze weekly journal entries using OpenAI

    Args:
        weekly_data: Dictionary with structure:
            {
                "patient_id": "...",
                "week_start": "YYYY-MM-DD",
                "week_end": "YYYY-MM-DD",
                "entries": [...]
            }
        model: OpenAI model to use (default: gpt-4)
        temperature: Model temperature (lower = more focused/deterministic)

    Returns:
        Dictionary with analysis results
    """
    # Initialize OpenAI client
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise Exception("OPENAI_API_KEY not found in environment variables")

    client = OpenAI(api_key=api_key)

    # Load and prepare prompt
    prompt_template = load_prompt_template()
    entries_formatted = format_entries_for_analysis(weekly_data)
    full_prompt = prompt_template.replace('{entries}', entries_formatted)

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a clinical psychology AI assistant helping therapists analyze patient journal entries for patterns and insights."
                },
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            temperature=temperature,
            response_format={"type": "json_object"}  # Ensures JSON response
        )

        # Parse the response
        analysis_text = response.choices[0].message.content
        analysis = json.loads(analysis_text)

        # Add metadata
        analysis['analysis_date'] = datetime.now().strftime('%Y-%m-%d')
        analysis['week_period'] = f"{weekly_data['week_start']} to {weekly_data['week_end']}"
        analysis['model_used'] = model
        analysis['entry_count'] = len(weekly_data.get('entries', []))

        return analysis

    except json.JSONDecodeError as e:
        # Fallback if JSON parsing fails
        return {
            "error": "Failed to parse GPT response as JSON",
            "raw_response": analysis_text,
            "exception": str(e)
        }

    except Exception as e:
        # Handle other errors
        return {
            "error": "Analysis failed",
            "exception": str(e),
            "week_period": f"{weekly_data['week_start']} to {weekly_data['week_end']}"
        }

def generate_summary_for_frontend(analysis):
    """
    Extract and format key information for frontend display

    Args:
        analysis: Full analysis dictionary from analyze_weekly_entries

    Returns:
        Simplified summary optimized for frontend
    """
    # Get primary theme (first pattern or default)
    theme = "Weekly Insights"
    if analysis.get('patterns') and len(analysis['patterns']) > 0:
        theme = analysis['patterns'][0].get('title', theme)

    return {
        "theme": theme,
        "summary": {
            "week_period": analysis.get('week_period', ''),
            "overall_mood": analysis.get('mood_trends', {}).get('overall_sentiment', 'neutral'),
            "sentiment_score": analysis.get('mood_trends', {}).get('sentiment_score', 0),
            "top_patterns": [
                {
                    "title": p.get('title'),
                    "description": p.get('description'),
                    "severity": p.get('severity', 'moderate')
                }
                for p in analysis.get('patterns', [])[:3]  # Top 3 patterns
            ],
            "key_topics": analysis.get('key_topics', [])[:5],  # Top 5 topics
            "clinical_prompts": analysis.get('clinical_prompts', []),
            "strengths": analysis.get('strengths_observed', []),
            "concerns": analysis.get('concerns', [])
        }
    }
