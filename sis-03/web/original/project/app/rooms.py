"""Room data for the Smart Campus Room Availability Checker.

Fictional sample data for demonstration only — no real bookings are
created or modified.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


# Campus operating window (minutes from 00:00).
OPEN_MIN = 0
CLOSE_MIN = 1440

# Maximum length of a single booking, in minutes.
MAX_DURATION = 120


@dataclass
class RoomBooking:
    id: str
    start: int  # minutes from 00:00
    end: int
    label: str


@dataclass
class Room:
    id: str
    name: str
    capacity: int
    building: str
    floor: int
    blocked: bool = False
    blocked_reason: Optional[str] = None
    bookings: list[RoomBooking] = field(default_factory=list)


ROOMS: list[Room] = [
    Room(
        id="r1",
        name="Thames Lecture Hall",
        capacity=200,
        building="East Wing",
        floor=1,
        bookings=[
            RoomBooking("b1", 540, 630, "CS101 Lecture"),
            RoomBooking("b2", 780, 840, "Faculty Meeting"),
        ],
    ),
    Room(
        id="r2",
        name="Turing Lab",
        capacity=40,
        building="Tech Block",
        floor=2,
        bookings=[
            RoomBooking("b3", 600, 720, "Robotics Workshop"),
            RoomBooking("b4", 840, 900, "Study Group"),
        ],
    ),
    Room(
        id="r3",
        name="Curie Seminar Room",
        capacity=16,
        building="Science Centre",
        floor=3,
        blocked=True,
        blocked_reason="Under maintenance — unavailable until further notice.",
        bookings=[
            RoomBooking("b5", 540, 600, "Reserved (blocked)"),
        ],
    ),
    Room(
        id="r4",
        name="Newton Study Lounge",
        capacity=60,
        building="Library",
        floor=1,
        bookings=[],
    ),
    Room(
        id="r5",
        name="Hawking Auditorium",
        capacity=300,
        building="Main Building",
        floor=0,
        bookings=[
            RoomBooking("b6", 720, 780, "Guest Lecture"),
            RoomBooking("b7", 900, 960, "Panel Discussion"),
        ],
    ),
    Room(
        id="r6",
        name="Darwin Project Room",
        capacity=8,
        building="Biosciences",
        floor=2,
        bookings=[
            RoomBooking("b8", 480, 540, "Team Standup"),
            RoomBooking("b9", 660, 720, "Thesis Review"),
            RoomBooking("b10", 960, 1020, "Lab Planning"),
        ],
    ),
]


def get_room(room_id: Optional[str]) -> Optional[Room]:
    if not room_id:
        return None
    return next((r for r in ROOMS if r.id == room_id), None)