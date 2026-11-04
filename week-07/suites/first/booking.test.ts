import { describe, expect, test } from 'vitest';
import { canBook } from './booking';

const fixture = () => ({
  now: 540,
  blocked: false,
  bookings: [{ start: 600, end: 660 }],
});

describe('canBook', () => {
  test('T01 AC4: touching after an existing booking is allowed', () => {
    expect(canBook({ ...fixture(), start: 660, end: 720 })).toBe(true);
  });

  test('T02 AC1: a request starting at the current time is rejected', () => {
    expect(canBook({ ...fixture(), start: 540, end: 570 })).toBe(false);
  });

  test('T03 AC1: a zero-duration request is rejected', () => {
    expect(canBook({ ...fixture(), start: 720, end: 720 })).toBe(false);
  });

  test('T04 AC1: a reversed request is rejected', () => {
    expect(canBook({ ...fixture(), start: 750, end: 720 })).toBe(false);
  });

  test('T05 AC1: a request ending after 24:00 is rejected', () => {
    expect(canBook({ ...fixture(), start: 1380, end: 1441 })).toBe(false);
  });

  test('T06 AC2: exactly 120 minutes is rejected', () => {
    expect(canBook({ ...fixture(), start: 720, end: 840 })).toBe(false);
  });

  test('T07 AC2: a 121-minute request is rejected', () => {
    expect(canBook({ ...fixture(), start: 720, end: 841 })).toBe(false);
  });

  test('T08 AC4: touching before an existing booking is allowed', () => {
    expect(canBook({ ...fixture(), start: 570, end: 600 })).toBe(true);
  });

  test('T09 AC4: a partial overlap is rejected', () => {
    expect(canBook({ ...fixture(), start: 630, end: 690 })).toBe(false);
  });

  test('T10 AC4: a request containing an existing booking is rejected', () => {
    expect(canBook({ ...fixture(), start: 570, end: 690 })).toBe(false);
  });

  test('T11 AC4: a request inside an existing booking is rejected', () => {
    expect(canBook({ ...fixture(), start: 615, end: 645 })).toBe(false);
  });

  test('T12 AC4: an identical interval is rejected', () => {
    expect(canBook({ ...fixture(), start: 600, end: 660 })).toBe(false);
  });

  test('T13 AC3: a blocked room is rejected', () => {
    expect(canBook({ ...fixture(), start: 660, end: 720, blocked: true })).toBe(false);
  });

  test('T14 AC4: a request is allowed when there are no existing bookings', () => {
    expect(canBook({ ...fixture(), start: 630, end: 690, bookings: [] })).toBe(true);
  });

  test('AC5: an available request does not change existing booking data', () => {
    const { bookings, ...request } = fixture();
    const before = structuredClone(bookings);

    expect(canBook({ ...request, start: 660, end: 720, bookings })).toBe(true);
    expect(bookings).toEqual(before);
  });

  test('X1 AC1: ending exactly at 24:00 is allowed', () => {
    expect(canBook({ ...fixture(), start: 1380, end: 1440 })).toBe(true);
  });

  test('X2 AC4: overlap with the second of multiple bookings is rejected', () => {
    expect(canBook({
      ...fixture(),
      start: 690,
      end: 730,
      bookings: [{ start: 600, end: 660 }, { start: 720, end: 780 }],
    })).toBe(false);
  });
});