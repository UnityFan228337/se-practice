interface TimeFieldProps {
  label: string;
  value: string;
  onChange: (v: string) => void;
  error?: string;
}

export default function TimeField({ label, value, onChange, error }: TimeFieldProps) {
  return (
    <div>
      <label className="block text-xs font-medium text-slate-600 mb-1">{label}</label>
      <input
        type="time"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className={[
          "w-full rounded-lg border px-3 py-2 text-sm text-slate-800 bg-white",
          "focus:outline-none focus:ring-2 transition-all",
          error
            ? "border-rose-300 focus:ring-rose-300/40"
            : "border-slate-300 focus:ring-sky-300/40 focus:border-sky-400",
        ].join(" ")}
      />
      {error && <p className="mt-1 text-xs text-rose-600">{error}</p>}
    </div>
  );
}
