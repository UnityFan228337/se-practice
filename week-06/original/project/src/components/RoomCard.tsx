import { Room, MAX_DURATION } from "@/data/rooms";
import { Users, Lock, MapPin, Building2 } from "lucide-react";

interface RoomCardProps {
  room: Room;
  selected: boolean;
  onSelect: () => void;
}

export default function RoomCard({ room, selected, onSelect }: RoomCardProps) {
  return (
    <button
      onClick={onSelect}
      disabled={room.blocked}
      className={[
        "w-full text-left rounded-xl border p-4 transition-all duration-200",
        room.blocked
          ? "border-slate-200 bg-slate-50 opacity-60 cursor-not-allowed"
          : selected
            ? "border-sky-500 bg-sky-50 ring-2 ring-sky-400/30 shadow-sm"
            : "border-slate-200 bg-white hover:border-sky-300 hover:shadow-sm",
      ].join(" ")}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <h3 className="font-semibold text-slate-800 text-sm truncate">{room.name}</h3>
          <div className="mt-1 flex flex-wrap items-center gap-x-3 gap-y-0.5 text-xs text-slate-500">
            <span className="inline-flex items-center gap-1">
              <MapPin className="w-3 h-3" /> Floor {room.floor}
            </span>
            <span className="inline-flex items-center gap-1">
              <Building2 className="w-3 h-3" /> {room.building}
            </span>
          </div>
        </div>
        <span className="inline-flex items-center gap-1 text-xs font-medium text-slate-600 shrink-0">
          <Users className="w-3.5 h-3.5" /> {room.capacity}
        </span>
      </div>

      {room.blocked ? (
        <div className="mt-2 inline-flex items-center gap-1 text-xs font-medium text-rose-600 bg-rose-50 px-2 py-0.5 rounded-full">
          <Lock className="w-3 h-3" /> Blocked
        </div>
      ) : (
        <div className="mt-2 text-xs text-slate-400">
          {room.bookings.length} existing booking{room.bookings.length === 1 ? "" : "s"} · max {MAX_DURATION} min
        </div>
      )}
    </button>
  );
}
