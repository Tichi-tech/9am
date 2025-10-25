const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000').replace(/\/$/, '');

export type Patient = {
  id: string;
  name: string;
  therapist?: string;
  entryCount: number;
  latestWeek?: {
    start: string | null;
    end: string | null;
  } | null;
};

export type Pattern = {
  name: string;
  severity: string;
  description: string;
};

export type WeeklyAnalysis = {
  id: string;
  patient_id: string;
  week_start: string;
  week_end: string;
  entries_analyzed: number;
  overall_mood: string;
  sentiment_score: number;
  themes: string;
  theme_title: string;
  patterns: Pattern[];
  mood_description: string;
  clinical_prompts: string[];
  strengths: string[];
  created_at: string;
};

type PatientResponse = {
  patients: Array<{
    patient_id: string;
    name?: string;
    therapist?: string;
    entry_count?: number;
    latest_week?: {
      start?: string;
      end?: string;
    } | null;
  }>;
};

type AnalysesResponse = {
  analyses: WeeklyAnalysis[];
};

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {}),
    },
    ...init,
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed: ${response.status}`);
  }

  return (await response.json()) as T;
}

export async function fetchPatients(): Promise<Patient[]> {
  const data = await request<PatientResponse>('/api/patients');

  return data.patients.map((patient) => ({
    id: patient.patient_id,
    name: patient.name || patient.patient_id,
    therapist: patient.therapist,
    entryCount: patient.entry_count ?? 0,
    latestWeek: patient.latest_week
      ? {
          start: patient.latest_week.start ?? null,
          end: patient.latest_week.end ?? null,
        }
      : null,
  }));
}

export async function fetchPatientAnalyses(patientId: string): Promise<WeeklyAnalysis[]> {
  const data = await request<AnalysesResponse>(`/api/patients/${patientId}/analyses`);
  return data.analyses;
}
