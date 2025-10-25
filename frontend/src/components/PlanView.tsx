import { WeeklyAnalysis } from '../lib/api';

interface PlanViewProps {
  analysis: WeeklyAnalysis | null;
}

export default function PlanView({ analysis }: PlanViewProps) {
  if (!analysis) {
    return (
      <div className="text-gray-900 text-lg">
        Select a patient or run the weekly pipeline to view a care plan.
      </div>
    );
  }

  if (!analysis.clinical_prompts || analysis.clinical_prompts.length === 0) {
    return (
      <div className="text-gray-900 text-lg">
        No clinical prompts available for this patient
      </div>
    );
  }

  const prompts = (analysis.clinical_prompts || []).slice(0, 5);

  return (
    <div className="flex flex-col gap-6 max-w-5xl">
      <div className="grid grid-cols-3 gap-6">
        {prompts.slice(0, 3).map((prompt, index) => (
          <div
            key={index}
            className="bg-white/40 backdrop-blur-sm p-8 shadow-sm"
          >
            <p className="text-gray-900 leading-relaxed text-[17px]">
              {prompt}
            </p>
          </div>
        ))}
      </div>

      {prompts.length > 3 && (
        <div className="grid grid-cols-3 gap-6">
          {prompts.slice(3, 5).map((prompt, index) => (
            <div
              key={index + 3}
              className="bg-white/40 backdrop-blur-sm p-8 shadow-sm"
            >
              <p className="text-gray-900 leading-relaxed text-[17px]">
                {prompt}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
