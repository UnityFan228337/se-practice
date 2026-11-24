import { describe, expect, test } from 'vitest';
import {
  explainAvailability,
  mockAdapter,
  type ExplainAdapter,
  type ExplainInput,
} from './explain';

const base: ExplainInput = {
  roomLabel: 'Room A-101',
  start: '11:00',
  end: '12:00',
  isAvailable: true,
  reasonCode: 'available',
};

describe('explainAvailability', () => {
  test('E1 available: the mock returns a generated agreement', async () => {
    const result = await explainAvailability(base, mockAdapter, 100);
    expect(result.explanation).toContain('available');
  });

  test('E2 overlap: the fallback agrees with an unavailable decision', async () => {
    const input = { ...base, isAvailable: false, reasonCode: 'overlap' as const };
    const result = await explainAvailability(input, mockAdapter, 100);
    expect(result.explanation).toContain('unavailable');
  });

  test('E3 blocked room: the mock explains the deterministic reason', async () => {
    const input = { ...base, isAvailable: false, reasonCode: 'room_blocked' as const };
    const result = await explainAvailability(input, mockAdapter, 100);
    expect(result.explanation).toContain('blocked');
  });

  test('E4 invalid time: malformed input gets fallback text', async () => {
    const input = { ...base, start: '25:00', reasonCode: 'invalid_time' as const, isAvailable: false };
    const result = await explainAvailability(input, mockAdapter, 100);
    expect(result.explanation).toContain('invalid');
  });

  test('E5 past time: a past request gets fallback text', async () => {
    const input = { ...base, isAvailable: false, reasonCode: 'past_time' as const };
    const result = await explainAvailability(input, mockAdapter, 100);
    expect(result.explanation).toContain('future');
  });

  test('E6 empty input: an empty room label uses a safe fallback', async () => {
    const input = { ...base, roomLabel: '' };
    const result = await explainAvailability(input, mockAdapter, 100);
    expect(result.explanation).toContain('Room');
  });

  test('E7 long input: labels over 60 characters are rejected', async () => {
    const input = { ...base, roomLabel: 'A'.repeat(61) };
    const result = await explainAvailability(input, mockAdapter, 100);
    expect(result.explanation).toContain('available');
  });

  test('E8 timeout: never-resolving adapter produces fallback', async () => {
    const slowAdapter: ExplainAdapter = () => new Promise(() => undefined);
    const result = await explainAvailability(base, slowAdapter, 5);
    expect(result.explanation).toContain('available');
  });

  test('E9 API failure: rejected adapter produces fallback', async () => {
    const failingAdapter: ExplainAdapter = async () => {
      throw new Error('simulated API failure');
    };
    const result = await explainAvailability(base, failingAdapter, 100);
    expect(result.explanation).toContain('available');
  });
});
