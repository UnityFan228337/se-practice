"""Availability-checking logic for the Room Availability Checker.

Mirrors the acceptance criteria used by the original implementation:
  AC1 interval within 0..1440 and start strictly after "now"
  AC2 no booking longer than 120 minutes
  AC3 reject when room is blocked
  AC4 reject overlap with existing bookings (touching endpoints allowed)
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .rooms import CLOSE_MIN, MAX_DURATION, OPEN_MIN, Room, RoomBooking


@dataclass
class AvailabilityResult:
    available: bool
    reason: str
    reason_key: str


def minutes_to_label(minutes: int) -> str:
    h, m = divmod(int(minutes), 60)
    return f"{h:02d}:{m:02d}"


def label_to_minutes(label: str) -> Optional[int]:
    """Return minutes-from-midnight, or None when the label is malformed."""
    if not label:
        return None
    try:
        h_str, m_str = label.split(":")
        h, m = int(h_str), int(m_str)
    except (ValueError, AttributeError):
        return None
    if not (0 <= h <= 23 and 0 <= m <= 59):
        return None
    return h * 60 + m


def _overlaps(a_start: int, a_end: int, b_start: int, b_end: int) -> bool:
    # Touching endpoints are NOT an overlap.
    return a_start < b_end and b_start < a_end


def check_overlap(start: int, end: int, booking: RoomBooking) -> bool:
    return _overlaps(start, end, booking.start, booking.end)


def check_availability(
    room: Optional[Room],
    start: Optional[int],
    end: Optional[int],
    current_minutes: int,
) -> AvailabilityResult:
    if room is None:
        return AvailabilityResult(
            False, "Select a room to check availability.", "no_room"
        )
    if start is None or end is None:
        return AvailabilityResult(
            False, "Enter a valid start and end time.", "invalid_input"
        )

    # AC1: in range and ordered, start after now
    if start < OPEN_MIN or end > CLOSE_MIN:
        return AvailabilityResult(
            False,
            f"Times must be between {minutes_to_label(OPEN_MIN)} and {minutes_to_label(CLOSE_MIN)}.",
            "out_of_range",
        )
    if start >= end:
        return AvailabilityResult(
            False, "Start time must be before end time.", "start_after_end"
        )
    if start <= current_minutes:
        return AvailabilityResult(
            False,
            f"Start time must be after the current time ({minutes_to_label(current_minutes)}).",
            "past_start",
        )

    # AC2: max duration
    if end - start > MAX_DURATION:
        return AvailabilityResult(
            False,
            f"Booking exceeds the {MAX_DURATION}-minute maximum ({end - start} min).",
            "too_long",
        )

    # AC3: blocked
    if room.blocked:
        return AvailabilityResult(
            False,
            room.blocked_reason or "This room is currently blocked.",
            "blocked",
        )

    # AC4: overlap
    conflict = next(
        (b for b in room.bookings if _overlaps(start, end, b.start, b.end)),
        None,
    )
    if conflict:
        return AvailabilityResult(
            False,
            f"Overlaps existing booking \"{conflict.label}\" "
            f"({minutes_to_label(conflict.start)}–{minutes_to_label(conflict.end)}).",
            "overlap",
        )

    return AvailabilityResult(
        True,
        f"Available for {end - start} min ({minutes_to_label(start)}–{minutes_to_label(end)}).",
        "available",
    )