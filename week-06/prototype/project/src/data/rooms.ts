export interface RoomBooking {
  id: string;
  start: number; // minutes from 00:00
  end: number;
  label: string;
}

export interface Room {
  id: string;
  name: string;
  capacity: number;
  building: string;
  floor: number;
  blocked: boolean;
  blockedReason?: string;
  bookings: RoomBooking[];
}

export const OPEN_MIN = 0;
export const CLOSE_MIN = 1440;
export const MAX_DURATION = 120;

export const rooms: Room[] = [
  {
    id: "r1",
    name: "Thames Lecture Hall",
    capacity: 200,
    building: "East Wing",
    floor: 1,
    blocked: false,
    bookings: [
      { id: "b1", start: 540, end: 630, label: "CS101 Lecture" },
      { id: "b2", start: 780, end: 840, label: "Faculty Meeting" },
    ],
  },
  {
    id: "r2",
    name: "Turing Lab",
    capacity: 40,
    building: "Tech Block",
    floor: 2,
    blocked: false,
    bookings: [
      { id: "b3", start: 600, end: 720, label: "Robotics Workshop" },
      { id: "b4", start: 840, end: 900, label: "Study Group" },
    ],
  },
  {
    id: "r3",
    name: "Curie Seminar Room",
    capacity: 16,
    building: "Science Centre",
    floor: 3,
    blocked: true,
    blockedReason: "Under maintenance — unavailable until further notice.",
    bookings: [
      { id: "b5", start: 540, end: 600, label: "Reserved (blocked)" },
    ],
  },
  {
    id: "r4",
    name: "Newton Study Lounge",
    capacity: 60,
    building: "Library",
    floor: 1,
    blocked: false,
    bookings: [],
  },
  {
    id: "r5",
    name: "Hawking Auditorium",
    capacity: 300,
    building: "Main Building",
    floor: 0,
    blocked: false,
    bookings: [
      { id: "b6", start: 720, end: 780, label: "Guest Lecture" },
      { id: "b7", start: 900, end: 960, label: "Panel Discussion" },
    ],
  },
  {
    id: "r6",
    name: "Darwin Project Room",
    capacity: 8,
    building: "Biosciences",
    floor: 2,
    blocked: false,
    bookings: [
      { id: "b8", start: 480, end: 540, label: "Team Standup" },
      { id: "b9", start: 660, end: 720, label: "Thesis Review" },
      { id: "b10", start: 960, end: 1020, label: "Lab Planning" },
    ],
  },
];
