import { Patient } from '../lib/api';

interface PatientListProps {
  patients: Patient[];
  selectedPatientId: string | null;
  onSelectPatient: (patientId: string) => void;
  isLoading?: boolean;
}

export default function PatientList({
  patients,
  selectedPatientId,
  onSelectPatient,
  isLoading,
}: PatientListProps) {
  return (
    <div className="flex flex-col gap-3">
      <h2 className="text-white/80 text-lg mb-2 font-light">Patient Portal</h2>
      {isLoading && (
        <div className="rounded-full bg-white/20 px-8 py-4 text-gray-800">
          Loading patients...
        </div>
      )}
      {!isLoading && patients.length === 0 && (
        <div className="rounded-3xl bg-white/20 px-6 py-4 text-gray-800">
          No patients available
        </div>
      )}
      {!isLoading &&
        patients.map((patient) => (
          <button
            key={patient.id}
            onClick={() => onSelectPatient(patient.id)}
            className={`px-8 py-4 rounded-full text-lg font-medium transition-all ${
              selectedPatientId === patient.id
                ? 'bg-white/30 text-gray-900'
                : 'bg-white/20 text-gray-800 hover:bg-white/25'
            }`}
          >
            {patient.name}
          </button>
        ))}
    </div>
  );
}
