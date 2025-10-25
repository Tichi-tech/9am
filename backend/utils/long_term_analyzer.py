"""
Long-term Trend Analyzer

Analyzes patterns across multiple weeks, months, or years of journal entries
"""
import os
import json
from datetime import datetime, timedelta
from openai import OpenAI

def get_all_entries_in_range(start_date, end_date, data_dir):
    """
    Collect all journal entries between two dates

    Args:
        start_date: Start date as string (YYYY-MM-DD)
        end_date: End date as string (YYYY-MM-DD)
        data_dir: Path to data directory

    Returns:
        List of all entries in chronological order
    """
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    all_entries = []
    current = start

    while current <= end:
        date_str = current.strftime('%Y-%m-%d')
        filepath = os.path.join(data_dir, f"{date_str}.json")

        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                entry = json.load(f)
                all_entries.append(entry)

        current += timedelta(days=1)

    return all_entries

def get_weekly_summaries_in_range(start_date, end_date, data_dir):
    """
    Collect all weekly summary files in a date range

    Args:
        start_date: Start date as string (YYYY-MM-DD)
        end_date: End date as string (YYYY-MM-DD)
        data_dir: Path to data directory

    Returns:
        List of weekly summary analyses
    """
    summaries = []

    # Find all weekly summary files
    for filename in os.listdir(data_dir):
        if filename.startswith('summary_') and filename.endswith('.json'):
            filepath = os.path.join(data_dir, filename)

            with open(filepath, 'r') as f:
                summary = json.load(f)

                # Check if this summary falls within our date range
                week_period = summary.get('week_period', '')
                if week_period:
                    # Parse week period (format: "YYYY-MM-DD to YYYY-MM-DD")
                    try:
                        week_start = week_period.split(' to ')[0].strip()
                        week_start_dt = datetime.strptime(week_start, '%Y-%m-%d')
                        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                        end_dt = datetime.strptime(end_date, '%Y-%m-%d')

                        if start_dt <= week_start_dt <= end_dt:
                            summaries.append(summary)
                    except:
                        pass

    # Sort by date
    summaries.sort(key=lambda x: x.get('week_period', ''))

    return summaries

def analyze_long_term_trends(start_date, end_date, data_dir, model="gpt-4o"):
    """
    Analyze trends across a longer time period (month/year)

    This function:
    1. Collects all weekly summaries in the range
    2. Uses GPT to identify meta-patterns across weeks
    3. Tracks progression/regression of issues
    4. Identifies long-term themes

    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        data_dir: Path to data directory
        model: OpenAI model to use

    Returns:
        Dictionary with long-term analysis
    """
    # Get all weekly summaries
    weekly_summaries = get_weekly_summaries_in_range(start_date, end_date, data_dir)

    if not weekly_summaries:
        return {
            "error": "No weekly summaries found in the specified range",
            "start_date": start_date,
            "end_date": end_date
        }

    # Format weekly summaries for GPT analysis
    summaries_text = format_weekly_summaries(weekly_summaries)

    # Create long-term analysis prompt
    prompt = f"""You are analyzing long-term patterns in a patient's journal entries.

You have access to {len(weekly_summaries)} weeks of analysis summaries from {start_date} to {end_date}.

Analyze these weekly summaries to identify:

1. **Meta-Patterns**: Recurring themes that persist across multiple weeks
2. **Trajectory**: Is the patient's emotional state improving, declining, or stable?
3. **Cyclical Patterns**: Do certain issues appear and disappear in cycles?
4. **Persistent Concerns**: What issues remain unresolved across the entire period?
5. **Progress Indicators**: What positive changes or coping improvements are evident?
6. **Treatment Recommendations**: Based on long-term patterns, what therapeutic approaches might be most effective?

Return your analysis in JSON format:
{{
  "analysis_period": "{start_date} to {end_date}",
  "weeks_analyzed": {len(weekly_summaries)},
  "meta_patterns": [
    {{
      "theme": "Theme name",
      "description": "Detailed description",
      "weeks_present": ["week1", "week2"],
      "severity_trend": "increasing|decreasing|stable",
      "first_observed": "date",
      "last_observed": "date"
    }}
  ],
  "trajectory": {{
    "overall_direction": "improving|declining|stable|fluctuating",
    "sentiment_progression": [-0.3, -0.2, -0.1, 0.0],
    "narrative": "Description of emotional trajectory"
  }},
  "cyclical_patterns": [
    {{
      "pattern": "Description",
      "frequency": "weekly|biweekly|monthly",
      "trigger": "If identifiable"
    }}
  ],
  "persistent_concerns": [
    {{
      "concern": "Issue description",
      "severity": "low|moderate|high",
      "weeks_present": 5,
      "evolution": "How it has changed over time"
    }}
  ],
  "progress_indicators": [
    "Positive changes observed"
  ],
  "treatment_recommendations": [
    {{
      "approach": "Therapeutic approach or intervention",
      "rationale": "Why this is recommended based on patterns",
      "priority": "high|medium|low"
    }}
  ]
}}

Weekly Summaries:
{summaries_text}
"""

    # Call OpenAI API
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise Exception("OPENAI_API_KEY not found in environment variables")

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert clinical psychologist analyzing long-term patient journal patterns."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        analysis = json.loads(response.choices[0].message.content)
        analysis['analysis_date'] = datetime.now().strftime('%Y-%m-%d')

        return analysis

    except Exception as e:
        return {
            "error": "Long-term analysis failed",
            "exception": str(e),
            "period": f"{start_date} to {end_date}"
        }

def format_weekly_summaries(summaries):
    """Format weekly summaries into text for GPT analysis"""
    formatted = []

    for summary in summaries:
        week_text = f"""
--- Week: {summary.get('week_period', 'Unknown')} ---
Entry Count: {summary.get('entry_count', 0)}
Overall Sentiment: {summary.get('mood_trends', {}).get('overall_sentiment', 'N/A')}
Sentiment Score: {summary.get('mood_trends', {}).get('sentiment_score', 'N/A')}

Key Patterns:
"""
        for pattern in summary.get('patterns', []):
            week_text += f"  - {pattern.get('title', 'N/A')} (severity: {pattern.get('severity', 'N/A')})\n"

        week_text += f"\nKey Topics:\n"
        for topic in summary.get('key_topics', []):
            week_text += f"  - {topic.get('topic', 'N/A')} ({topic.get('count', 0)}x)\n"

        week_text += f"\nClinical Prompts:\n"
        for prompt in summary.get('clinical_prompts', [])[:3]:
            week_text += f"  - {prompt}\n"

        formatted.append(week_text)

    return '\n'.join(formatted)

def compare_time_periods(period1_start, period1_end, period2_start, period2_end, data_dir, model="gpt-4o"):
    """
    Compare two time periods (e.g., this month vs last month, this year vs last year)

    Useful for tracking improvement over time

    Args:
        period1_start, period1_end: First time period
        period2_start, period2_end: Second time period
        data_dir: Path to data directory
        model: OpenAI model

    Returns:
        Comparison analysis
    """
    period1_analysis = analyze_long_term_trends(period1_start, period1_end, data_dir, model)
    period2_analysis = analyze_long_term_trends(period2_start, period2_end, data_dir, model)

    return {
        "period_1": {
            "range": f"{period1_start} to {period1_end}",
            "analysis": period1_analysis
        },
        "period_2": {
            "range": f"{period2_start} to {period2_end}",
            "analysis": period2_analysis
        },
        "comparison_summary": generate_comparison_summary(period1_analysis, period2_analysis)
    }

def generate_comparison_summary(analysis1, analysis2):
    """Generate a summary comparing two time periods"""
    # Simple comparison - can be enhanced with GPT
    summary = {
        "sentiment_change": "N/A",
        "pattern_evolution": "N/A",
        "improvement_noted": False
    }

    # Compare sentiment trajectories
    if 'trajectory' in analysis1 and 'trajectory' in analysis2:
        dir1 = analysis1['trajectory'].get('overall_direction', '')
        dir2 = analysis2['trajectory'].get('overall_direction', '')

        if dir1 == 'declining' and dir2 == 'improving':
            summary['sentiment_change'] = "Significant improvement"
            summary['improvement_noted'] = True
        elif dir1 == 'improving' and dir2 == 'declining':
            summary['sentiment_change'] = "Concerning decline"
        else:
            summary['sentiment_change'] = f"Period 1: {dir1}, Period 2: {dir2}"

    return summary
