import { AvailabilityResult } from "@/lib/availability";
import { CheckCircle2, XCircle, Info } from "lucide-react";

interface ResultBannerProps {
  result: AvailabilityResult;
  checked: boolean;
}

export default function ResultBanner({ result, checked }: ResultBannerProps) {
  if (!checked) {
    return (
      <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 flex items-center gap-3">
        <Info className="w-5 h-5 text-slate-400 shrink-0" />
        <p className="text-sm text-slate-500">
          Pick a room and enter a time range, then press <strong>Check Availability</strong>.
        </p>
      </div>
    );
  }

  const isAvailable = result.available;
  return (
    <div
      className={[
        "rounded-xl border p-4 flex items-start gap-3 transition-all duration-300",
        isAvailable
          ? "border-emerald-300 bg-emerald-50"
          : "border-rose-300 bg-rose-50",
      ].join(" ")}
    >
      {isAvailable ? (
        <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
      ) : (
        <XCircle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
      )}
      <div>
        <p className={["font-semibold text-sm", isAvailable ? "text-emerald-800" : "text-rose-800"].join(" ")}>
          {isAvailable ? "Available" : "Unavailable"}
        </p>
        <p className={["text-sm mt-0.5", isAvailable ? "text-emerald-700" : "text-rose-700"].join(" ")}>
          {result.reason}
        </p>
      </div>
    </div>
  );
}
