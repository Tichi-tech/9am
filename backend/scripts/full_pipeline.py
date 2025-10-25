"""Run the full Therapist Copilot pipeline from raw journal JSON entries.

This command-line helper lets a therapist (or operator) ingest a batch of
entries, aggregate them into a weekly packet, run the GPT-based analysis, and
emit a human-friendly report that surfaces patterns often missed during live
sessions.

Usage example:

    python backend/scripts/full_pipeline.py \
        --patient-id maya-thompson \
        --week-start 2025-01-12 \
        --week-end 2025-01-18 \
        --entries-file data/maya-thompson/new_entries.json

If you already have per-day JSON files under `data/<patient_id>/`, omit
`--entries-file` and the script will reuse what is on disk.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from utils.analyzer import analyze_weekly_entries
 
DATA_DIR = BASE_DIR / 'data'


@dataclass
class PipelineResult:
    patient_id: str
    week_start: str
    week_end: str
    entry_count: int
    weekly_file: Path
    summary_file: Path
    report_file: Path
    analysis: Dict[str, Any]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Therapist Copilot pipeline end to end")
    parser.add_argument('--patient-id', required=True, help='Identifier that maps to data/<patient_id>')
    parser.add_argument('--week-start', required=True, help='Week start date (YYYY-MM-DD)')
    parser.add_argument('--week-end', required=True, help='Week end date (YYYY-MM-DD)')
    parser.add_argument('--entries-file', help='Optional JSON file containing daily entries to ingest before running')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing daily JSON files when ingesting entries')
    parser.add_argument('--report-format', choices=['markdown', 'text'], default='markdown', help='Format of the saved therapist report')
    return parser.parse_args()


def ensure_patient_dir(patient_id: str) -> Path:
    patient_dir = DATA_DIR / patient_id
    patient_dir.mkdir(parents=True, exist_ok=True)
    return patient_dir


def load_entries_from_file(path: Path) -> List[Dict[str, Any]]:
    with path.open('r') as f:
        payload = json.load(f)

    if isinstance(payload, dict) and 'entries' in payload:
        entries = payload['entries']
    elif isinstance(payload, list):
        entries = payload
    else:
        raise ValueError('Entries file must be a list or contain an "entries" array')

    normalized = []
    for idx, entry in enumerate(entries, start=1):
        if 'date' not in entry:
            raise ValueError(f'Entry #{idx} is missing a "date" field')
        if 'text' not in entry:
            raise ValueError(f'Entry #{idx} is missing a "text" field')

        normalized.append({
            'patient_id': entry.get('patient_id'),
            'date': entry['date'],
            'time': entry.get('time', ''),
            'text': entry['text'],
            'metadata': entry.get('metadata', {}),
        })

    return normalized


def ingest_entries(entries: List[Dict[str, Any]], patient_dir: Path, overwrite: bool = False) -> None:
    for entry in entries:
        entry_date = entry['date']
        target_path = patient_dir / f'{entry_date}.json'
        if target_path.exists() and not overwrite:
            continue

        with target_path.open('w') as f:
            json.dump(entry, f, indent=2)


def aggregate_week(patient_id: str, patient_dir: Path, week_start: str, week_end: str) -> Dict[str, Any]:
    start_dt = datetime.strptime(week_start, '%Y-%m-%d')
    end_dt = datetime.strptime(week_end, '%Y-%m-%d')

    entries: List[Dict[str, Any]] = []
    current = start_dt
    missing_days: List[str] = []

    while current <= end_dt:
        date_str = current.strftime('%Y-%m-%d')
        path = patient_dir / f'{date_str}.json'
        if path.exists():
            with path.open('r') as f:
                entries.append(json.load(f))
        else:
            missing_days.append(date_str)
        current += timedelta(days=1)

    if not entries:
        raise FileNotFoundError('No daily JSON files found for the requested week')

    weekly_data = {
        'patient_id': patient_id,
        'week_start': week_start,
        'week_end': week_end,
        'entries': entries,
        'missing_days': missing_days,
    }

    weekly_filename = f'week_{week_start}_to_{week_end}.json'
    weekly_path = patient_dir / weekly_filename
    with weekly_path.open('w') as f:
        json.dump(weekly_data, f, indent=2)

    return weekly_data


def save_summary(patient_dir: Path, week_start: str, week_end: str, analysis: Dict[str, Any]) -> Path:
    summary_filename = f'summary_{week_start}_to_{week_end}.json'
    summary_path = patient_dir / summary_filename
    with summary_path.open('w') as f:
        json.dump(analysis, f, indent=2)
    return summary_path


def build_report_text(weekly_data: Dict[str, Any], analysis: Dict[str, Any]) -> str:
    patterns = analysis.get('patterns', [])
    mood = analysis.get('mood_trends', {})
    prompts = analysis.get('clinical_prompts', [])
    strengths = analysis.get('strengths_observed', [])
    concerns = analysis.get('concerns', [])

    lines = [
        f"# Therapist Briefing — {weekly_data['week_start']} to {weekly_data['week_end']}",
        f"**Patient:** {weekly_data.get('patient_id', 'Unknown')}",
        '',
        '## Snapshot',
        f"- Entries analyzed: {len(weekly_data.get('entries', []))}",
        f"- Missing daily journals: {len(weekly_data.get('missing_days', []))}",
        f"- Mood trend: {mood.get('overall_sentiment', 'unknown')} (score {mood.get('sentiment_score', 0)})",
        f"- Theme focus: {patterns[0].get('title', 'N/A') if patterns else 'N/A'}",
        '',
    ]

    if patterns:
        lines.append('## Hidden Patterns Worth Surfacing')
        for pattern in patterns:
            lines.append(f"- **{pattern.get('title', pattern.get('name', 'Pattern'))}** ({pattern.get('severity', 'moderate')}): {pattern.get('description', '')}")
        lines.append('')

    if prompts:
        lines.append('## Therapist Prompts for Next Session')
        for prompt in prompts:
            lines.append(f"- {prompt}")
        lines.append('')

    if strengths:
        lines.append('## Patient Strengths to Reinforce')
        for strength in strengths:
            lines.append(f"- {strength}")
        lines.append('')

    if concerns:
        lines.append('## Emerging Risks / Unspoken Concerns')
        for concern in concerns:
            lines.append(f"- {concern}")
        lines.append('')

    summary_paragraph = analysis.get('summary_text') or analysis.get('summary') or ''
    if summary_paragraph:
        lines.append('## Narrative Summary')
        lines.append(summary_paragraph)
        lines.append('')

    lines.append('_Generated via Therapist Copilot full pipeline_')
    return '\n'.join(lines).strip()


def save_report(patient_dir: Path, week_start: str, week_end: str, report_text: str, fmt: str) -> Path:
    extension = 'md' if fmt == 'markdown' else 'txt'
    report_path = patient_dir / f'report_{week_start}_to_{week_end}.{extension}'
    with report_path.open('w') as f:
        f.write(report_text)
    return report_path


def run_pipeline(args: argparse.Namespace) -> PipelineResult:
    patient_dir = ensure_patient_dir(args.patient_id)

    if args.entries_file:
        entries = load_entries_from_file(Path(args.entries_file))
        ingest_entries(entries, patient_dir, overwrite=args.overwrite)

    weekly_data = aggregate_week(args.patient_id, patient_dir, args.week_start, args.week_end)
    analysis = analyze_weekly_entries(weekly_data)

    # Include a synthesized summary for the report if not present
    if 'summary_text' not in analysis:
        summary_text = (
            f"Week of {args.week_start} to {args.week_end}. "
            f"Analyzed {len(weekly_data['entries'])} entries; overall mood {analysis.get('mood_trends', {}).get('overall_sentiment', 'neutral')}."
        )
        analysis['summary_text'] = summary_text

    summary_file = save_summary(patient_dir, args.week_start, args.week_end, analysis)
    report_text = build_report_text(weekly_data, analysis)
    report_file = save_report(patient_dir, args.week_start, args.week_end, report_text, args.report_format)

    return PipelineResult(
        patient_id=args.patient_id,
        week_start=args.week_start,
        week_end=args.week_end,
        entry_count=len(weekly_data['entries']),
        weekly_file=patient_dir / f'week_{args.week_start}_to_{args.week_end}.json',
        summary_file=summary_file,
        report_file=report_file,
        analysis=analysis,
    )


def main() -> None:
    args = parse_args()
    try:
        result = run_pipeline(args)
    except Exception as exc:
        print(f"\n❌ Pipeline failed: {exc}\n")
        raise

    print('\n✅ Full pipeline complete')
    print(f"Patient: {result.patient_id}")
    print(f"Week: {result.week_start} → {result.week_end}")
    print(f"Entries analyzed: {result.entry_count}")
    print(f"Weekly packet saved to: {result.weekly_file}")
    print(f"Summary JSON saved to: {result.summary_file}")
    print(f"Therapist report saved to: {result.report_file}\n")

    print('Top clinical prompts:')
    for prompt in (result.analysis.get('clinical_prompts') or [])[:3]:
        print(f" - {prompt}")


if __name__ == '__main__':
    main()
