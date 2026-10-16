import { Room, OPEN_MIN, CLOSE_MIN } from "@/data/rooms";
import { checkOverlap } from "@/lib/availability";

interface TimelineProps {
  room: Room;
  candidateStart: number | null;
  candidateEnd: number | null;
  currentMinutes: number;
}

export default function Timeline({ room, candidateStart, candidateEnd, currentMinutes }: TimelineProps) {
  const span = CLOSE_MIN - OPEN_MIN;

  const pct = (min: number) => ((min - OPEN_MIN) / span) * 100;

  const hourMarks = Array.from({ length: 25 }, (_, i) => i * 60);

  return (
    <div className="mt-4">
      <div className="relative h-12 rounded-lg bg-slate-100 border border-slate-200 overflow-hidden">
        {/* Existing bookings */}
        {room.bookings.map((b) => (
          <div
            key={b.id}
            className="absolute top-0 bottom-0 bg-slate-400/60 border-x border-slate-500/40 flex items-center justify-center overflow-hidden group"
            style={{ left: `${pct(b.start)}%`, width: `${pct(b.end) - pct(b.start)}%` }}
            title={`${b.label} (${b.start}–${b.end})`}
          >
            <span className="text-[10px] text-white font-medium truncate px-1 hidden sm:block">
              {b.label}
            </span>
          </div>
        ))}

        {/* Current time marker */}
        <div
          className="absolute top-0 bottom-0 w-px bg-amber-500 z-10"
          style={{ left: `${pct(currentMinutes)}%` }}
          title="Now"
        >
          <div className="absolute -top-0 -translate-x-1/2 w-2 h-2 rounded-full bg-amber-500" />
        </div>

        {/* Candidate interval preview */}
        {candidateStart !== null && candidateEnd !== null && candidateStart < candidateEnd && (
          (() => {
            const overlap = room.bookings.some((b) => checkOverlap(candidateStart, candidateEnd, b));
            const blocked = room.blocked;
            const color = overlap || blocked ? "bg-rose-400/50" : "bg-emerald-400/50";
            return (
              <div
                className={`absolute top-0 bottom-0 ${color} border-2 border-dashed ${
                  overlap || blocked ? "border-rose-500" : "border-emerald-500"
                } z-10`}
                style={{ left: `${pct(candidateStart)}%`, width: `${pct(candidateEnd) - pct(candidateStart)}%` }}
              />
            );
          })()
        )}
      </div>

      {/* Hour axis */}
      <div className="relative h-5 mt-1">
        {hourMarks.filter((_, i) => i % 3 === 0).map((m) => (
          <div key={m} className="absolute text-[10px] text-slate-400 -translate-x-1/2" style={{ left: `${pct(m)}%` }}>
            {String(Math.floor(m / 60)).padStart(2, "0")}:00
          </div>
        ))}
      </div>
    </div>
  );
}
