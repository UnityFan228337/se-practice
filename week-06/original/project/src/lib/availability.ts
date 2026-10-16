import { Room, RoomBooking, OPEN_MIN, CLOSE_MIN, MAX_DURATION } from "@/data/rooms";

export interface AvailabilityResult {
  available: boolean;
  reason: string;
  reasonKey: string;
}

export function minutesToLabel(min: number): string {
  const h = Math.floor(min / 60);
  const m = min % 60;
  return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}`;
}

export function labelToMinutes(label: string): number {
  const [h, m] = label.split(":").map(Number);
  return h * 60 + m;
}

function overlaps(aStart: number, aEnd: number, bStart: number, bEnd: number): boolean {
  return aStart < bEnd && bStart < aEnd;
}

export function checkAvailability(
  room: Room | null,
  start: number | null,
  end: number | null,
  currentMinutes: number
): AvailabilityResult {
  if (!room) {
    return { available: false, reason: "Select a room to check availability.", reasonKey: "no_room" };
  }
  if (start === null || end === null || isNaN(start) || isNaN(end)) {
    return { available: false, reason: "Enter a valid start and end time.", reasonKey: "invalid_input" };
  }

  // AC1: interval must satisfy 0 ≤ start < end ≤ 1440 and start after current time
  if (start < OPEN_MIN || end > CLOSE_MIN) {
    return {
      available: false,
      reason: `Times must be between ${minutesToLabel(OPEN_MIN)} and ${minutesToLabel(CLOSE_MIN)}.`,
      reasonKey: "out_of_range",
    };
  }
  if (start >= end) {
    return { available: false, reason: "Start time must be before end time.", reasonKey: "start_after_end" };
  }
  if (start < currentMinutes) {
    return {
      available: false,
      reason: `Start time must be after the current time (${minutesToLabel(currentMinutes)}).`,
      reasonKey: "past_start",
    };
  }

  // AC2: reject bookings longer than 120 minutes
  if (end - start > MAX_DURATION) {
    return {
      available: false,
      reason: `Booking exceeds the ${MAX_DURATION}-minute maximum (${end - start} min).`,
      reasonKey: "too_long",
    };
  }

  // AC3: reject when room is blocked
  if (room.blocked) {
    return {
      available: false,
      reason: room.blockedReason ?? "This room is currently blocked.",
      reasonKey: "blocked",
    };
  }

  // AC4: reject overlap with existing bookings (touching endpoints allowed)
  const conflict = room.bookings.find((b) => overlaps(start, end, b.start, b.end));
  if (conflict) {
    return {
      available: false,
      reason: `Overlaps existing booking "${conflict.label}" (${minutesToLabel(conflict.start)}–${minutesToLabel(conflict.end)}).`,
      reasonKey: "overlap",
    };
  }

  return {
    available: true,
    reason: `Available for ${end - start} min (${minutesToLabel(start)}–${minutesToLabel(end)}).`,
    reasonKey: "available",
  };
}

export function checkOverlap(start: number, end: number, booking: RoomBooking): boolean {
  return overlaps(start, end, booking.start, booking.end);
}
