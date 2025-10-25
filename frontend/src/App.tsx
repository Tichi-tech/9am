import { useState, useEffect } from 'react';
import {
  fetchPatients,
  fetchPatientAnalyses,
  Patient,
  WeeklyAnalysis,
} from './lib/api';
import PatientList from './components/PatientList';
import SummaryView from './components/SummaryView';
import ThemeView from './components/ThemeView';
import PlanView from './components/PlanView';
import DemoView from './components/DemoView';

type Tab = 'demo' | 'summary' | 'theme' | 'plan';

export default function App() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [selectedPatientId, setSelectedPatientId] = useState<string | null>(null);
  const [analyses, setAnalyses] = useState<WeeklyAnalysis[]>([]);
  const [activeTab, setActiveTab] = useState<Tab>('demo');
  const [currentTime, setCurrentTime] = useState(new Date());
  const [isLoadingPatients, setIsLoadingPatients] = useState(true);
  const [isLoadingAnalyses, setIsLoadingAnalyses] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 60000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    const loadPatients = async () => {
      try {
        setIsLoadingPatients(true);
        setError(null);
        const data = await fetchPatients();
        setPatients(data);
        setSelectedPatientId((current) => current ?? data[0]?.id ?? null);
      } catch (err) {
        console.error('Error fetching patients:', err);
        setError(err instanceof Error ? err.message : 'Unable to load patients');
      } finally {
        setIsLoadingPatients(false);
      }
    };

    loadPatients();
  }, []);

  useEffect(() => {
    if (!selectedPatientId) {
      setAnalyses([]);
      return;
    }

    const loadAnalyses = async () => {
      try {
        setIsLoadingAnalyses(true);
        setError(null);
        const data = await fetchPatientAnalyses(selectedPatientId);
        setAnalyses(data);
      } catch (err) {
        console.error('Error fetching analyses:', err);
        setError(err instanceof Error ? err.message : 'Unable to load analyses');
        setAnalyses([]);
      } finally {
        setIsLoadingAnalyses(false);
      }
    };

    loadAnalyses();
  }, [selectedPatientId]);

  const formatTime = () => {
    return currentTime.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
  };

  const latestAnalysis = analyses.length > 0 ? analyses[0] : null;

  return (
    <div className="min-h-screen p-8" style={{ backgroundColor: '#BB8D8D' }}>
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-white text-5xl font-light mb-2">{formatTime()}</h1>
          <p className="text-white/80 text-lg">Therapist Copilot Dashboard</p>
        </div>

        {/* Demo Section - Separate from Patient Views */}
        {activeTab === 'demo' && (
          <div className="mb-8">
            <div className="bg-white/20 backdrop-blur-sm rounded-2xl p-4 mb-4">
              <h2 className="text-white text-2xl font-light">Interactive Demo</h2>
              <p className="text-white/90 text-sm mt-1">
                See how the AI analyzes a week of journal entries. Then explore real patient data below.
              </p>
            </div>
            <DemoView />
          </div>
        )}

        {activeTab !== 'demo' && (
          <div className="flex gap-8">
          <div className="w-56 flex-shrink-0">
            <PatientList
              patients={patients}
              selectedPatientId={selectedPatientId}
              onSelectPatient={setSelectedPatientId}
              isLoading={isLoadingPatients}
            />
          </div>

          <div className="flex-1">
            {error && (
              <div className="mb-4 rounded-2xl bg-red-100/70 px-6 py-4 text-red-900">
                {error}
              </div>
            )}
            <div className="flex gap-4 mb-8">
              <button
                onClick={() => setActiveTab('demo')}
                className={`px-12 py-4 rounded-full text-lg font-medium transition-all ${
                  activeTab === 'demo'
                    ? 'bg-white/40 text-gray-900'
                    : 'bg-white/20 text-gray-800 hover:bg-white/25'
                }`}
              >
                ✨ Demo
              </button>
              <button
                onClick={() => setActiveTab('summary')}
                className={`px-12 py-4 rounded-full text-lg font-medium transition-all ${
                  activeTab === 'summary'
                    ? 'bg-white/40 text-gray-900'
                    : 'bg-white/20 text-gray-800 hover:bg-white/25'
                }`}
              >
                Summary
              </button>
              <button
                onClick={() => setActiveTab('theme')}
                className={`px-12 py-4 rounded-full text-lg font-medium transition-all ${
                  activeTab === 'theme'
                    ? 'bg-white/40 text-gray-900'
                    : 'bg-white/20 text-gray-800 hover:bg-white/25'
                }`}
              >
                Theme
              </button>
              <button
                onClick={() => setActiveTab('plan')}
                className={`px-12 py-4 rounded-full text-lg font-medium transition-all ${
                  activeTab === 'plan'
                    ? 'bg-white/40 text-gray-900'
                    : 'bg-white/20 text-gray-800 hover:bg-white/25'
                }`}
              >
                Plan
              </button>
            </div>

            <div className="min-h-[600px]">
              {isLoadingAnalyses ? (
                <div className="text-gray-900 text-lg">Loading weekly insights...</div>
              ) : (
                <>
                  {activeTab === 'summary' && <SummaryView analyses={analyses} />}
                  {activeTab === 'theme' && <ThemeView analysis={latestAnalysis} />}
                  {activeTab === 'plan' && <PlanView analysis={latestAnalysis} />}
                </>
              )}
            </div>
          </div>
        </div>
        )}

        {/* Navigation Tabs */}
        {activeTab !== 'demo' && (
          <div className="mt-8 flex justify-center">
            <button
              onClick={() => setActiveTab('demo')}
              className="px-6 py-3 bg-white/30 hover:bg-white/40 text-white rounded-full text-sm font-medium transition-all"
            >
              ← Back to Interactive Demo
            </button>
          </div>
        )}

        {activeTab === 'demo' && (
          <div className="mt-8 bg-white/20 backdrop-blur-sm rounded-2xl p-6">
            <h3 className="text-white text-xl font-light mb-4">Explore Real Patient Data</h3>
            <p className="text-white/90 mb-4">
              See actual analyses for 3 patients with different therapeutic scenarios
            </p>
            <button
              onClick={() => setActiveTab('summary')}
              className="px-8 py-3 bg-white/40 hover:bg-white/50 text-gray-900 rounded-full font-medium transition-all"
            >
              View Patient Dashboard →
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
