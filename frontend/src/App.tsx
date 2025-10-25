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

type Tab = 'summary' | 'theme' | 'plan';

export default function App() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [selectedPatientId, setSelectedPatientId] = useState<string | null>(null);
  const [analyses, setAnalyses] = useState<WeeklyAnalysis[]>([]);
  const [activeTab, setActiveTab] = useState<Tab>('summary');
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
        <div className="mb-12">
          <h1 className="text-white text-5xl font-light mb-2">{formatTime()}</h1>
        </div>

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
      </div>
    </div>
  );
}
