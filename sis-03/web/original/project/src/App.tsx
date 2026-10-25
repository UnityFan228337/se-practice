import { useState, useMemo, useCallback } from "react";
import { rooms, Room, OPEN_MIN, CLOSE_MIN, MAX_DURATION } from "@/data/rooms";
import {
  checkAvailability,
  minutesToLabel,
  labelToMinutes,
  AvailabilityResult,
} from "@/lib/availability";
import RoomCard from "@/components/RoomCard";
import Timeline from "@/components/Timeline";
import ResultBanner from "@/components/ResultBanner";
import TimeField from "@/components/TimeField";
import { Clock, CalendarCheck, Search, RotateCcw } from "lucide-react";

export default function App() {
  const [selectedRoomId, setSelectedRoomId] = useState<string | null>(null);
  const [startTime, setStartTime] = useState("10:00");
  const [endTime, setEndTime] = useState("11:00");
  const [result, setResult] = useState<AvailabilityResult | null>(null);
  const [checked, setChecked] = useState(false);

  const currentMinutes = useMemo(() => {
    const now = new Date();
    return now.getHours() * 60 + now.getMinutes();
  }, []);

  const selectedRoom: Room | null = useMemo(
    () => rooms.find((r) => r.id === selectedRoomId) ?? null,
    [selectedRoomId]
  );

  const startMin = useMemo(() => {
    if (!startTime) return null;
    const m = labelToMinutes(startTime);
    return isNaN(m) ? null : m;
  }, [startTime]);

  const endMin = useMemo(() => {
    if (!endTime) return null;
    const m = labelToMinutes(endTime);
    return isNaN(m) ? null : m;
  }, [endTime]);

  const startError = useMemo(() => {
    if (startMin === null) return "Required";
    if (startMin < OPEN_MIN || startMin >= CLOSE_MIN) return `Must be ${minutesToLabel(OPEN_MIN)}–${minutesToLabel(CLOSE_MIN)}`;
    if (startMin < currentMinutes) return `Must be after now (${minutesToLabel(currentMinutes)})`;
    return undefined;
  }, [startMin, currentMinutes]);

  const endError = useMemo(() => {
    if (endMin === null) return "Required";
    if (endMin <= OPEN_MIN || endMin > CLOSE_MIN) return `Must be ${minutesToLabel(OPEN_MIN)}–${minutesToLabel(CLOSE_MIN)}`;
    if (startMin !== null && endMin <= startMin) return "Must be after start";
    if (startMin !== null && endMin - startMin > MAX_DURATION) return `Max ${MAX_DURATION} min`;
    return undefined;
  }, [endMin, startMin]);

  const handleCheck = useCallback(() => {
    setResult(checkAvailability(selectedRoom, startMin, endMin, currentMinutes));
    setChecked(true);
  }, [selectedRoom, startMin, endMin, currentMinutes]);

  const handleReset = useCallback(() => {
    setSelectedRoomId(null);
    setStartTime("10:00");
    setEndTime("11:00");
    setResult(null);
    setChecked(false);
  }, []);

  const livePreview = useMemo(() => {
    return checkAvailability(selectedRoom, startMin, endMin, currentMinutes);
  }, [selectedRoom, startMin, endMin, currentMinutes]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-sky-50/40 to-slate-100">
      {/* Header */}
      <header className="border-b border-slate-200/70 bg-white/80 backdrop-blur-sm sticky top-0 z-20">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-sky-500 to-cyan-600 flex items-center justify-center shadow-sm">
              <CalendarCheck className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-slate-800 leading-tight">Room Availability Checker</h1>
              <p className="text-xs text-slate-500 hidden sm:block">Smart Campus · Northgate University</p>
            </div>
          </div>
          <div className="inline-flex items-center gap-2 text-xs text-slate-500 bg-slate-100 px-3 py-1.5 rounded-full">
            <Clock className="w-3.5 h-3.5" />
            <span className="font-medium tabular-nums">{minutesToLabel(currentMinutes)}</span>
            <span className="text-slate-400 hidden sm:inline">· campus time</span>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 sm:px-6 py-6 lg:py-8">
        <div className="grid lg:grid-cols-5 gap-6">
          {/* Room list */}
          <section className="lg:col-span-2">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm font-semibold text-slate-700">Rooms</h2>
              <span className="text-xs text-slate-400">{rooms.length} total</span>
            </div>
            <div className="space-y-2.5">
              {rooms.map((room) => (
                <RoomCard
                  key={room.id}
                  room={room}
                  selected={selectedRoomId === room.id}
                  onSelect={() => setSelectedRoomId(room.id)}
                />
              ))}
            </div>
          </section>

          {/* Checker panel */}
          <section className="lg:col-span-3">
            <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5 sm:p-6">
              <h2 className="text-sm font-semibold text-slate-700 mb-4">Check a time interval</h2>

              <div className="grid sm:grid-cols-2 gap-4">
                <TimeField label="Start time" value={startTime} onChange={setStartTime} error={startError} />
                <TimeField label="End time" value={endTime} onChange={setEndTime} error={endError} />
              </div>

              <div className="mt-4 flex flex-wrap gap-2 text-xs text-slate-400">
                <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-slate-50 border border-slate-200">
                  Range {minutesToLabel(OPEN_MIN)}–{minutesToLabel(CLOSE_MIN)}
                </span>
                <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-slate-50 border border-slate-200">
                  Max {MAX_DURATION} min
                </span>
                <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-slate-50 border border-slate-200">
                  Touching endpoints OK
                </span>
              </div>

              <div className="mt-5 flex gap-3">
                <button
                  onClick={handleCheck}
                  disabled={!selectedRoomId}
                  className={[
                    "inline-flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all",
                    selectedRoomId
                      ? "bg-sky-600 text-white hover:bg-sky-700 shadow-sm hover:shadow"
                      : "bg-slate-200 text-slate-400 cursor-not-allowed",
                  ].join(" ")}
                >
                  <Search className="w-4 h-4" /> Check Availability
                </button>
                <button
                  onClick={handleReset}
                  className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium text-slate-600 hover:bg-slate-100 transition-colors"
                >
                  <RotateCcw className="w-4 h-4" /> Reset
                </button>
              </div>

              {selectedRoom ? (
                <>
                  <div className="mt-6 border-t border-slate-100 pt-5">
                    <div className="flex items-center justify-between mb-1">
                      <h3 className="text-sm font-semibold text-slate-700">
                        {selectedRoom.name} — today
                      </h3>
                      <span className="text-xs text-slate-400">00:00 → 24:00</span>
                    </div>
                    <p className="text-xs text-slate-500 mb-2">
                      Existing bookings shown in grey. Your candidate interval shows green (free) or red (conflict).
                    </p>
                    <Timeline
                      room={selectedRoom}
                      candidateStart={startMin}
                      candidateEnd={endMin}
                      currentMinutes={currentMinutes}
                    />
                  </div>

                  {/* Live preview hint */}
                  <div className="mt-4 text-xs text-slate-500 bg-slate-50 rounded-lg px-3 py-2 border border-slate-100">
                    <span className="font-medium text-slate-600">Live preview:</span>{" "}
                    {livePreview.available ? "Looks available" : livePreview.reasonKey === "no_room" ? "—" : livePreview.reason}
                  </div>
                </>
              ) : (
                <div className="mt-6 text-center py-10 border-2 border-dashed border-slate-200 rounded-xl">
                  <CalendarCheck className="w-8 h-8 text-slate-300 mx-auto mb-2" />
                  <p className="text-sm text-slate-400">Select a room to view its schedule and timeline.</p>
                </div>
              )}
            </div>

            {/* Result banner */}
            <div className="mt-4">
              <ResultBanner result={result ?? { available: false, reason: "", reasonKey: "none" }} checked={checked} />
            </div>
          </section>
        </div>

        <footer className="mt-8 text-center text-xs text-slate-400">
          Fictional sample data for demonstration only · No real bookings are created or modified.
        </footer>
      </main>
    </div>
  );
}
