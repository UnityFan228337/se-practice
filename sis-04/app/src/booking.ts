import type { Room } from './rooms';

export type BookingRequest = {
  start: number;
  end: number;
  now: number;
  blocked: boolean;
  bookings: { start: number; end: number }[];
};

export function canBook({ start, end, now, blocked, bookings }: BookingRequest): boolean {
  if (!(start >= 0 && end <= 1440 && now >= 0 && now <= 1440)) {
    return false;
  }

  if (!(start < end)) {
    return false;
  }

  if (!(start > now)) {
    return false;
  }

  if (end - start > 120) {
    return false;
  }

  if (blocked) {
    return false;
  }

  for (const booking of bookings) {
    if (start < booking.end && end > booking.start) {
      return false;
    }
  }

  return true;
}

export function checkRoom(
  rooms: Room[],
  roomId: string,
  request: { start: number; end: number; now: number },
): boolean {
  const room = rooms.find((candidate) => candidate.id === roomId);

  if (!room) {
    return false;
  }

  return canBook({
    start: request.start,
    end: request.end,
    now: request.now,
    blocked: room.blocked,
    bookings: room.bookings,
  });
}
