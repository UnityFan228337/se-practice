export type Room = {
  id: string;
  name: string;
  capacity: number;
  equipment: string[];
  blocked: boolean;
  bookings: { start: number; end: number }[];
};

export const ROOMS: Room[] = [
  {
    id: 'a101',
    name: 'A-101',
    capacity: 8,
    equipment: ['projector', 'whiteboard'],
    blocked: false,
    bookings: [{ start: 600, end: 660 }],
  },
  {
    id: 'b204',
    name: 'B-204',
    capacity: 12,
    equipment: ['projector', 'whiteboard', 'video'],
    blocked: false,
    bookings: [{ start: 720, end: 780 }],
  },
  {
    id: 'c310',
    name: 'C-310',
    capacity: 20,
    equipment: ['whiteboard', 'monitor', 'video'],
    blocked: true,
    bookings: [{ start: 540, end: 600 }],
  },
  {
    id: 'd420',
    name: 'D-420',
    capacity: 30,
    equipment: ['projector', 'whiteboard', 'audio'],
    blocked: false,
    bookings: [{ start: 900, end: 960 }, { start: 1020, end: 1080 }],
  },
  {
    id: 'e505',
    name: 'E-505',
    capacity: 6,
    equipment: ['whiteboard'],
    blocked: false,
    bookings: [],
  },
];
