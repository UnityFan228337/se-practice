import { describe, expect, test } from 'vitest';
import { canBook, checkRoom } from './booking';
import { filterRooms } from './filter';
import type { Room } from './rooms';

const testRooms: Room[] = [
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

describe('booking rules', () => {
  test('AC1: start must be before end', () => {
    expect(
      canBook({ start: 600, end: 600, now: 540, blocked: false, bookings: [] }),
    ).toBe(false);
  });

  test('AC1: requests in the past are rejected', () => {
    expect(
      canBook({ start: 540, end: 600, now: 600, blocked: false, bookings: [] }),
    ).toBe(false);
  });

  test('AC2 B1: exactly 120 minutes is available', () => {
    expect(
      canBook({ start: 540, end: 660, now: 500, blocked: false, bookings: [] }),
    ).toBe(true);
  });

  test('AC2 B2: 121 minutes is rejected', () => {
    expect(
      canBook({ start: 540, end: 661, now: 500, blocked: false, bookings: [] }),
    ).toBe(false);
  });

  test('AC3: blocked room is rejected', () => {
    expect(
      canBook({ start: 540, end: 600, now: 500, blocked: true, bookings: [] }),
    ).toBe(false);
  });

  test('AC4 B3: touching an existing booking is allowed', () => {
    expect(
      canBook({ start: 660, end: 720, now: 500, blocked: false, bookings: [{ start: 600, end: 660 }] }),
    ).toBe(true);
  });

  test('AC4 B4: overlapping an existing booking is rejected', () => {
    expect(
      canBook({ start: 620, end: 700, now: 500, blocked: false, bookings: [{ start: 600, end: 660 }] }),
    ).toBe(false);
  });

  test('AC5: canBook does not mutate the bookings list', () => {
    const bookings = [{ start: 600, end: 660 }];
    const original = [...bookings];

    canBook({ start: 720, end: 780, now: 500, blocked: false, bookings });

    expect(bookings).toEqual(original);
  });

  test('F3: blocked room cannot be reported as available', () => {
    expect(checkRoom(testRooms, 'c310', { start: 660, end: 720, now: 600 })).toBe(false);
  });

  test('F5 INT: a different selected room refreshes the result', () => {
    expect(checkRoom(testRooms, 'a101', { start: 690, end: 750, now: 600 })).toBe(true);
    expect(checkRoom(testRooms, 'b204', { start: 690, end: 750, now: 600 })).toBe(false);
    expect(checkRoom(testRooms, 'e505', { start: 690, end: 750, now: 600 })).toBe(true);
  });
});

describe('filter rules', () => {
  test('F1 B5: capacity exactly equal to attendees is included', () => {
    const rooms = filterRooms(testRooms, { attendees: 8, equipment: [] });
    expect(rooms.some((room) => room.id === 'a101')).toBe(true);
  });

  test('F1 B6: capacity one below attendees is excluded', () => {
    const rooms = filterRooms(testRooms, { attendees: 7, equipment: [] });
    expect(rooms.some((room) => room.id === 'e505')).toBe(false);
  });

  test('F2: room must include all selected equipment', () => {
    const rooms = filterRooms(testRooms, { attendees: 8, equipment: ['projector', 'video'] });
    expect(rooms.some((room) => room.id === 'b204')).toBe(true);
    expect(rooms.some((room) => room.id === 'a101')).toBe(false);
  });

  test('F4: no room matches the filter shows an empty result', () => {
    const rooms = filterRooms(testRooms, { attendees: 50, equipment: ['projector'] });
    expect(rooms).toHaveLength(0);
  });

  test('INT: filterRooms plus checkRoom returns a consistent answer', () => {
    const rooms = filterRooms(testRooms, { attendees: 8, equipment: ['projector'] });
    const selected = rooms[0];
    expect(selected).toBeDefined();
    expect(checkRoom(rooms, selected.id, { start: 720, end: 780, now: 600 })).toBe(true);
  });
});
