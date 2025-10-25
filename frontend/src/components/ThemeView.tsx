import { WeeklyAnalysis } from '../lib/api';

interface ThemeViewProps {
  analysis: WeeklyAnalysis | null;
}

export default function ThemeView({ analysis }: ThemeViewProps) {
  if (!analysis) {
    return (
      <div className="text-gray-900 text-lg">
        Select a patient or run a weekly analysis to view themes.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="border-l-2 border-gray-800/30 pl-6">
        <h3 className="text-gray-900 text-xl font-medium mb-6">
          Theme: {analysis.theme_title}
        </h3>

        <div className="space-y-6">
          <div>
            <h4 className="text-gray-900 font-medium mb-3">Patterns Identified:</h4>
            <ol className="list-decimal list-inside space-y-2">
              {(analysis.patterns || []).map((pattern, index) => (
                <li key={index} className="text-gray-900">
                  {pattern.name} ({pattern.severity}) - {pattern.description}
                </li>
              ))}
            </ol>
          </div>

          <div>
            <p className="text-gray-900">
              <span className="font-medium">Mood:</span> {analysis.mood_description}
            </p>
          </div>

          <div>
            <h4 className="text-gray-900 font-medium mb-3">Clinical Prompts for Therapist:</h4>
            <ul className="space-y-2">
              {analysis.clinical_prompts.map((prompt, index) => (
                <li key={index} className="text-gray-900">
                  - {prompt}
                </li>
              ))}
            </ul>
          </div>

          <div>
            <p className="text-gray-900">
              <span className="font-medium">Strengths:</span> {analysis.strengths}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
