export type Interval = { start: number; end: number };

export type BookingRequest = {
  start: number;
  end: number;
  now: number;
  blocked: boolean;
  bookings: Interval[];
};

export type AvailabilityResult = {
  result: boolean | null;
  error: string;
};

export type AvailabilityReason =
  | 'available'
  | 'invalid_time'
  | 'past_time'
  | 'too_long'
  | 'room_blocked'
  | 'overlap';

export function availabilityReason({ start, end, now, blocked, bookings }: BookingRequest): AvailabilityReason {
  if (!(0 <= start && start < end && end <= 1440)) return 'invalid_time';
  if (!(start > now)) return 'past_time';
  if (end - start > 120) return 'too_long';
  if (blocked) return 'room_blocked';

  for (const booking of bookings) {
    if (start < booking.end && end > booking.start) return 'overlap';
  }

  return 'available';
}

export function canBook(request: BookingRequest): boolean {
  return availabilityReason(request) === 'available';
}

export function evaluateAvailability(request: BookingRequest): AvailabilityResult {
  if (!(request.start < request.end)) {
    return { result: null, error: 'The end time must be after the start time.' };
  }

  return { result: canBook(request), error: '' };
}
