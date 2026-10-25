"""Shared serialization so templates and the JSON API return the same shapes."""
from __future__ import annotations

from typing import Any

from .availability import AvailabilityResult, minutes_to_label
from .rooms import CLOSE_MIN, MAX_DURATION, OPEN_MIN, Room


def room_to_dict(room: Room) -> dict[str, Any]:
    return {
        "id": room.id,
        "name": room.name,
        "capacity": room.capacity,
        "building": room.building,
        "floor": room.floor,
        "blocked": room.blocked,
        "blocked_reason": room.blocked_reason,
        "bookings": [
            {
                "id": b.id,
                "start": b.start,
                "end": b.end,
                "label": b.label,
                "start_label": minutes_to_label(b.start),
                "end_label": minutes_to_label(b.end),
            }
            for b in room.bookings
        ],
    }


def result_to_dict(result: AvailabilityResult) -> dict[str, Any]:
    return {
        "available": result.available,
        "reason": result.reason,
        "reason_key": result.reason_key,
    }


def campus_config() -> dict[str, Any]:
    return {
        "open_min": OPEN_MIN,
        "close_min": CLOSE_MIN,
        "max_duration": MAX_DURATION,
        "open_label": minutes_to_label(OPEN_MIN),
        "close_label": minutes_to_label(CLOSE_MIN),
    }