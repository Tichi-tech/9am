import { WeeklyAnalysis } from '../lib/api';

interface SummaryViewProps {
  analyses: WeeklyAnalysis[];
}

export default function SummaryView({ analyses }: SummaryViewProps) {
  if (analyses.length === 0) {
    return (
      <div className="text-gray-900 text-lg">
        No weekly summaries are available yet.
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {analyses.map((analysis) => (
        <div key={analysis.id} className="grid grid-cols-[auto_1fr] gap-6 items-start">
          <div className="space-y-1 text-gray-900 min-w-[280px]">
            <p className="font-normal">Week Period: {analysis.week_start} to {analysis.week_end}</p>
            <p>Entries Analyzed: {analysis.entries_analyzed}</p>
            <p>Overall Mood: {analysis.overall_mood}</p>
            <p>Sentiment Score: {analysis.sentiment_score}</p>
          </div>
          <div className="bg-white/20 rounded-3xl px-8 py-6">
            <p className="text-gray-900 leading-relaxed text-[17px]">
              {analysis.themes}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}
