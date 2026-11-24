export type AvailabilityReason =
  | 'available'
  | 'invalid_time'
  | 'past_time'
  | 'too_long'
  | 'room_blocked'
  | 'overlap';

export type ExplainInput = {
  roomLabel: string;
  start: string;
  end: string;
  isAvailable: boolean;
  reasonCode: AvailabilityReason;
};

export type ExplainAdapter = (input: ExplainInput) => Promise<{ explanation: string }>;

export const SYSTEM_INSTRUCTION =
  'Use only the supplied room, start, end, availability status and deterministic reason code. ' +
  'Say whether the room is available or unavailable without inventing details or extra times.';

const TIME_PATTERN = /^([01]\d|2[0-3]):[0-5]\d$/;
const reasonCodes = new Set<AvailabilityReason>([
  'available',
  'invalid_time',
  'past_time',
  'too_long',
  'room_blocked',
  'overlap',
]);

const fallbackText: Record<AvailabilityReason, string> = {
  available: 'The room is available for the requested time.',
  invalid_time: 'The room is unavailable because the requested time is invalid.',
  past_time: 'The room is unavailable because the start time is not in the future.',
  too_long: 'The room is unavailable because the request is longer than 120 minutes.',
  room_blocked: 'The room is unavailable because the room is blocked.',
  overlap: 'The room is unavailable because the request overlaps an existing booking.',
};

export function fallbackExplanation(input: ExplainInput): string {
  const prefix = input.roomLabel.trim();
  return `${fallbackText[input.reasonCode]} Room: ${prefix}.`;
}

export const mockAdapter: ExplainAdapter = async (input) => {
  if (input.isAvailable) {
    return { explanation: `Room ${input.roomLabel.trim()} is available from ${input.start} to ${input.end}.` };
  }
  const reason = fallbackText[input.reasonCode].replace('The room', `Room ${input.roomLabel.trim()}`);
  return { explanation: `${reason} Requested time: ${input.start}-${input.end}.` };
};

function validateInput(input: ExplainInput): string | null {
  if (!input || typeof input.roomLabel !== 'string') return 'Invalid room label.';
  const label = input.roomLabel.trim();
  if (label.length < 1 || label.length > 60) return 'Invalid room label.';
  if (!TIME_PATTERN.test(input.start) || (!TIME_PATTERN.test(input.end) && input.end !== '24:00')) return 'Invalid time.';
  if (typeof input.isAvailable !== 'boolean') return 'Invalid availability.';
  if (!reasonCodes.has(input.reasonCode)) return 'Invalid reason code.';
  return null;
}

function sentenceCount(text: string): number {
  const sentences = text.split(/[.!?]+/).filter((part) => part.trim().length > 0);
  return sentences.length;
}

function validateOutput(input: ExplainInput, output: unknown): output is { explanation: string } {
  if (!output || typeof output !== 'object') return false;
  const explanation = (output as { explanation?: unknown }).explanation;
  if (typeof explanation !== 'string') return false;
  const text = explanation.trim();
  if (!text || text.length > 280 || sentenceCount(text) > 2) return false;

  const lower = text.toLowerCase();
  const hasAvailable = /\bavailable\b/.test(lower);
  const hasUnavailable = /\bunavailable\b/.test(lower);
  if (input.isAvailable && (!hasAvailable || hasUnavailable)) return false;
  if (!input.isAvailable && (!hasUnavailable || hasAvailable)) return false;

  const times = text.match(/\b([01]\d|2[0-3]):[0-5]\d\b/g) ?? [];
  const requested = new Set([input.start, input.end]);
  if (times.some((time) => !requested.has(time))) return false;
  return true;
}

export async function explainAvailability(
  input: ExplainInput,
  adapter: ExplainAdapter,
  timeoutMs: number,
): Promise<{ explanation: string }> {
  const invalid = validateInput(input);
  if (invalid) return { explanation: fallbackExplanation(input) };
  if (!Number.isFinite(timeoutMs) || timeoutMs <= 0) return { explanation: fallbackExplanation(input) };

  let timer: ReturnType<typeof setTimeout> | undefined;
  const timeout = new Promise<never>((_, reject) => {
    timer = setTimeout(() => reject(new Error('Explanation timeout')), timeoutMs);
  });

  try {
    const output = await Promise.race([adapter(input), timeout]);
    if (!validateOutput(input, output)) return { explanation: fallbackExplanation(input) };
    return { explanation: output.explanation.trim() };
  } catch {
    return { explanation: fallbackExplanation(input) };
  } finally {
    if (timer) clearTimeout(timer);
  }
}
