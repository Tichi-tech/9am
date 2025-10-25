import { useState } from 'react';
import { FileText, Sparkles, Clock, DollarSign, Calendar } from 'lucide-react';

const DEMO_WEEK_ENTRIES = [
  {
    date: "Monday, Feb 10",
    text: "Can't sleep again. Mind won't shut off. Keep replaying that meeting where I froze up. Everyone probably thinks I'm incompetent."
  },
  {
    date: "Tuesday, Feb 11",
    text: "Woke up with that familiar weight on my chest. Called in sick. I know I should push through but I just can't today."
  },
  {
    date: "Wednesday, Feb 12",
    text: "Mom texted asking how I'm doing. Didn't respond. What would I even say? She wouldn't understand."
  },
  {
    date: "Thursday, Feb 13",
    text: "Panic attack at the grocery store. Had to abandon my cart and leave. The cashier was staring. So embarrassed."
  },
  {
    date: "Friday, Feb 14",
    text: "Jake invited me to game night. Made up an excuse. I know they'll stop inviting me eventually. Maybe that's for the best."
  },
  {
    date: "Saturday, Feb 15",
    text: "Therapy tomorrow. Part of me doesn't want to go. What's the point? We just talk in circles."
  },
  {
    date: "Sunday, Feb 16",
    text: "First session focusing on anxiety. Therapist wants me to try breathing exercises. Feels pointless but I'll try. What do I have to lose?"
  }
];

const DEMO_INSIGHTS = {
  theme: "Anxiety with Avoidance Patterns and Social Isolation",
  patterns: [
    {
      name: "Recurring Panic/Anxiety Episodes",
      severity: "high",
      description: "Multiple anxiety episodes across the week (Mon work meeting, Thu grocery store). Pattern shows anxiety triggered by both professional and everyday situations, indicating generalized anxiety rather than situation-specific.",
      frequency: "3 of 7 days"
    },
    {
      name: "Progressive Social Withdrawal",
      severity: "high",
      description: "Consistent pattern of avoiding social connections throughout the week: not responding to Mom (Wed), canceling with Jake (Fri), calling in sick (Tue). Pattern escalates from passive avoidance to active isolation.",
      frequency: "5 of 7 days"
    },
    {
      name: "Negative Self-Talk and Rumination",
      severity: "moderate",
      description: "Persistent negative thought patterns visible across entries: 'incompetent' (Mon), 'she wouldn't understand' (Wed), 'they'll stop inviting me' (Fri). Shows cognitive distortion loop.",
      frequency: "4 of 7 days"
    },
    {
      name: "Ambivalence Toward Treatment",
      severity: "moderate",
      description: "Conflicting feelings about therapy evident in Sat/Sun entries: 'what's the point' vs 'I'll try'. This ambivalence is common early in treatment but worth addressing.",
      frequency: "2 of 7 days"
    }
  ],
  clinicalPrompts: [
    "Explore the escalation pattern: anxiety episodes are happening in multiple contexts (work, public spaces). Consider discussing generalized anxiety disorder screening.",
    "Address social withdrawal urgently - pattern shows active avoidance of support network (Mom, Jake). Discuss connection between isolation and worsening symptoms.",
    "Work on cognitive restructuring for negative thought patterns. Patient shows awareness ('what would I even say?') which is a therapeutic opening.",
    "Validate and address therapy ambivalence directly. Patient's willingness to 'try' despite doubts is a strength to build on.",
    "The breathing exercise mention (Sunday) shows engagement with treatment - reinforce this and expand coping toolkit."
  ],
  sentiment: -0.48,
  mood: "consistently negative with slight openness at week end",
  strengths: [
    "Maintained daily journaling throughout the week - shows commitment to treatment",
    "Self-awareness evident in multiple entries (recognizes patterns, understands consequences)",
    "Willingness to try coping strategies despite skepticism (breathing exercises Sunday)",
    "Attended therapy session and engaged with homework despite ambivalence"
  ],
  weekSummary: "Week of Feb 10-16, 2025. Analyzed 7 journal entries. Patient shows high anxiety with avoidance patterns escalating through mid-week, followed by slight treatment engagement toward week end."
};

export default function DemoView() {
  const [showInsights, setShowInsights] = useState(false);

  return (
    <div className="space-y-6">
      {/* Hero Section */}
      <div className="bg-white/30 backdrop-blur-sm rounded-2xl p-8 mb-8">
        <h2 className="text-3xl font-light text-gray-900 mb-4">
          How Therapist Copilot Works
        </h2>
        <p className="text-lg text-gray-800 mb-6">
          Watch AI analyze a <strong>week of journal entries</strong> and surface emotional patterns across multiple days.
        </p>

        {/* Value Props */}
        <div className="grid grid-cols-4 gap-4 mb-6">
          <div className="bg-white/40 rounded-xl p-4">
            <Calendar className="w-6 h-6 text-gray-700 mb-2" />
            <div className="text-2xl font-semibold text-gray-900">7 days</div>
            <div className="text-sm text-gray-700">Weekly analysis</div>
          </div>
          <div className="bg-white/40 rounded-xl p-4">
            <Clock className="w-6 h-6 text-gray-700 mb-2" />
            <div className="text-2xl font-semibold text-gray-900">25-40min</div>
            <div className="text-sm text-gray-700">Saved per week</div>
          </div>
          <div className="bg-white/40 rounded-xl p-4">
            <Sparkles className="w-6 h-6 text-gray-700 mb-2" />
            <div className="text-2xl font-semibold text-gray-900">3-5sec</div>
            <div className="text-sm text-gray-700">AI analysis time</div>
          </div>
          <div className="bg-white/40 rounded-xl p-4">
            <DollarSign className="w-6 h-6 text-gray-700 mb-2" />
            <div className="text-2xl font-semibold text-gray-900">$0.02</div>
            <div className="text-sm text-gray-700">Cost per week</div>
          </div>
        </div>
      </div>

      {/* Before/After Comparison */}
      <div className="grid grid-cols-2 gap-6">
        {/* BEFORE: Raw Journal */}
        <div className="space-y-4">
          <div className="flex items-center gap-2 mb-4">
            <FileText className="w-5 h-5 text-gray-700" />
            <h3 className="text-xl font-medium text-gray-900">
              BEFORE: One Week of Journal Entries
            </h3>
          </div>

          <div className="bg-white/40 backdrop-blur-sm rounded-2xl p-6 max-h-[500px] overflow-y-auto">
            <div className="text-sm font-semibold text-gray-600 mb-4">
              📅 Week of Feb 10-16, 2025 (7 entries)
            </div>
            <div className="space-y-4">
              {DEMO_WEEK_ENTRIES.map((entry, i) => (
                <div key={i} className="border-l-2 border-gray-300 pl-4 pb-3">
                  <div className="text-xs font-semibold text-gray-600 mb-1">
                    {entry.date}
                  </div>
                  <div className="text-sm text-gray-800 leading-relaxed">
                    {entry.text}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white/30 rounded-xl p-4 text-sm text-gray-700">
            <strong>Traditional Approach:</strong>
            <ul className="mt-2 space-y-1 ml-4">
              <li>• Read 7 entries: 10-15 min</li>
              <li>• Identify patterns manually: 15-20 min</li>
              <li>• Connect themes across days: 5-10 min</li>
              <li>• Prepare session notes: 5-10 min</li>
              <li><strong>• TOTAL: 35-55 minutes per week</strong></li>
            </ul>
          </div>
        </div>

        {/* AFTER: AI Insights */}
        <div className="space-y-4">
          <div className="flex items-center gap-2 mb-4">
            <Sparkles className="w-5 h-5 text-gray-700" />
            <h3 className="text-xl font-medium text-gray-900">
              AFTER: What Therapist Gets
            </h3>
          </div>

          {!showInsights ? (
            <div className="bg-white/40 backdrop-blur-sm rounded-2xl p-12 flex flex-col items-center justify-center h-[400px]">
              <Sparkles className="w-16 h-16 text-gray-400 mb-4" />
              <button
                onClick={() => setShowInsights(true)}
                className="px-8 py-4 bg-white/60 hover:bg-white/80 text-gray-900 rounded-full text-lg font-medium transition-all shadow-lg hover:shadow-xl"
              >
                ✨ Run AI Analysis
              </button>
              <p className="text-sm text-gray-600 mt-4">Click to see the magic</p>
            </div>
          ) : (
            <div className="space-y-4 animate-fade-in">
              {/* Theme */}
              <div className="bg-white/50 backdrop-blur-sm rounded-2xl p-6">
                <div className="text-xs font-semibold text-gray-600 mb-2">PRIMARY THEME</div>
                <div className="text-xl font-medium text-gray-900">
                  {DEMO_INSIGHTS.theme}
                </div>
              </div>

              {/* Week Summary */}
              <div className="bg-white/50 backdrop-blur-sm rounded-2xl p-6">
                <div className="text-xs font-semibold text-gray-600 mb-2">WEEK SUMMARY</div>
                <p className="text-sm text-gray-800">{DEMO_INSIGHTS.weekSummary}</p>
              </div>

              {/* Patterns */}
              <div className="bg-white/50 backdrop-blur-sm rounded-2xl p-6">
                <div className="text-xs font-semibold text-gray-600 mb-3">PATTERNS DETECTED ACROSS WEEK</div>
                <div className="space-y-3">
                  {DEMO_INSIGHTS.patterns.map((pattern, i) => (
                    <div key={i} className="border-l-4 border-gray-700/30 pl-4">
                      <div className="flex items-center gap-2 mb-1 flex-wrap">
                        <span className="font-medium text-gray-900">{pattern.name}</span>
                        <span className={`text-xs px-2 py-0.5 rounded-full ${
                          pattern.severity === 'high' ? 'bg-red-100 text-red-800' :
                          pattern.severity === 'moderate' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'
                        }`}>
                          {pattern.severity}
                        </span>
                        <span className="text-xs px-2 py-0.5 rounded-full bg-blue-100 text-blue-800">
                          {pattern.frequency}
                        </span>
                      </div>
                      <p className="text-sm text-gray-700">{pattern.description}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Clinical Actions */}
              <div className="bg-white/50 backdrop-blur-sm rounded-2xl p-6">
                <div className="text-xs font-semibold text-gray-600 mb-3">CLINICAL ACTION ITEMS</div>
                <div className="space-y-2">
                  {DEMO_INSIGHTS.clinicalPrompts.map((prompt, i) => (
                    <div key={i} className="flex gap-2 text-sm text-gray-800">
                      <span className="text-gray-600">{i + 1}.</span>
                      <span>{prompt}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Strengths */}
              <div className="bg-white/50 backdrop-blur-sm rounded-2xl p-6">
                <div className="text-xs font-semibold text-gray-600 mb-3">PATIENT STRENGTHS</div>
                <div className="space-y-2">
                  {DEMO_INSIGHTS.strengths.map((strength, i) => (
                    <div key={i} className="flex gap-2 text-sm text-gray-800">
                      <span className="text-green-600">✓</span>
                      <span>{strength}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-green-50/50 rounded-xl p-4 text-sm text-gray-700 border-2 border-green-200/50">
                <strong>✨ With Therapist Copilot:</strong>
                <ul className="mt-2 space-y-1 ml-4">
                  <li>• AI analyzes all 7 entries: 3-5 seconds</li>
                  <li>• Identifies 4 major patterns across the week</li>
                  <li>• Tracks frequency and progression</li>
                  <li>• Therapist review of insights: 3-5 minutes</li>
                  <li><strong>• TOTAL: ~5 minutes (90% time saved!)</strong></li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Key Benefits */}
      {showInsights && (
        <div className="bg-white/40 backdrop-blur-sm rounded-2xl p-8 animate-fade-in">
          <h3 className="text-2xl font-light text-gray-900 mb-6">Why This Matters</h3>
          <div className="grid grid-cols-2 gap-6">
            <div>
              <h4 className="font-semibold text-gray-900 mb-3">For Therapists:</h4>
              <ul className="space-y-2 text-sm text-gray-800">
                <li>• Save 11+ hours/week with typical caseload</li>
                <li>• Never miss important emotional patterns</li>
                <li>• Better prepared = better sessions</li>
                <li>• Reduce burnout from manual analysis</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-3">For Patients:</h4>
              <ul className="space-y-2 text-sm text-gray-800">
                <li>• More focused, effective therapy sessions</li>
                <li>• Concrete evidence of progress over time</li>
                <li>• Therapist understands your journey deeper</li>
                <li>• Better outcomes, faster improvement</li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
