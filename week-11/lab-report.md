# Week 11 - Lab report

**Name:** Maltsev Yaroslav
**Group:** 25B
**Date:** 24 November 2026

---

## 1. Setup

| | |
| --- | --- |
| Assistant I built the feature with (tool) | GitHub Copilot in VS Code |
| Its exact model (with its version, or `not displayed`) | not displayed |
| Assistant I reviewed with (tool) | VS Code code-review agent |
| Its exact model (with its version, or `not displayed`) | not displayed |
| Starting point (`week-10` or `week-08`) | week-10 |
| Baseline commit - the checkpoint of Part 0 | 5680dc7 |
| Where I ran the tests (Bolt terminal / my computer / Codespace) | my computer |
| Vitest version (the `RUN  v…` line of a run) | 3.2.7 |

---

## 2. Task 1 - the baseline

### 2.1 The project's commands

| Command | Exists | Result | Note |
| --- | --- | --- | --- |
| `npx vitest run` | yes | pass | 18 existing tests passed before feature changes |
| `npm run build` | yes | pass | Vite/TypeScript production build succeeded |
| `npm run lint` | no | not run | No lint script exists in the Week 10 package |

### 2.2 The baseline test run

```text
RUN  v3.2.7 C:/Users/yar/Desktop/se/se-practice/week-11/app

✓ src/booking.test.ts (18 tests) 8ms
Test Files  1 passed (1)
Tests 18 passed (18)
Duration 506ms
```

### 2.3 What I located

| What | Where (file, and the function or component name) |
| --- | --- |
| The availability function | `week-11/app/src/booking.ts`, `canBook` |
| The UI component | `week-11/app/src/App.tsx`, `App` |
| The repository instructions | `week-11/app/AGENTS.md` |

---

## 3. Task 2 - the feature, defined before the code

### 3.1 The user story

Add an optional "Explain availability" feature: given a room, requested time and deterministic
availability result, generate a short student-friendly explanation.
The existing booking rules remain the source of truth. The LLM must never decide availability or
change bookings.

### 3.2 The contract

| Field | Direction | Type / format | Validation |
| --- | --- | --- | --- |
| `roomLabel` | input | string, 1-60 characters after trimming | reject null, empty or over 60 characters |
| `start` | input | `"HH:MM"` | reject malformed or out-of-range time |
| `end` | input | `"HH:MM"` | reject malformed or out-of-range time; allow `24:00` in the UI |
| `isAvailable` | input | boolean | reject non-booleans and conflicts with `reasonCode` |
| `reasonCode` | input | one of six deterministic codes | reject unknown code and status/code conflict |
| `explanation` | output | string, at most 280 chars and two sentences | reject empty, contradictory, too long, extra-sentence or invented-time output |

### 3.3 Acceptance criteria and failure behaviour

F1 Existing availability and overlap rules remain unchanged.

F2 The explanation agrees with the deterministic result; no invented booking details.

F3 Empty, malformed or overly long input is rejected.

F4 API timeout, error or unavailable key produces a safe fallback.

F5 A user can distinguish generated explanation from confirmed booking status.

| Failure | What the student sees |
| --- | --- |
| Invalid input (empty, malformed, too long) | The confirmed status remains separate and a deterministic explanation fallback is shown |
| The model times out | The status stays unchanged; the page shows the safe deterministic fallback |
| The model fails (error, no key) | The status stays unchanged; the page shows the mock-style generated fallback |
| The model's answer contradicts the decision, or invents a detail | The contradictory answer is discarded and replaced by a deterministic fallback |

### 3.4 The flow

```text
student input -> validation -> availabilityReason/canBook -> { isAvailable, reasonCode }
                                                                |
                                                    availabilityReason decides reason
                                                                |
                                    App passes structured input to mockAdapter
                                                                |
                                         explainAvailability validates output
                                                                |
                             UI shows confirmed status apart from generated explanation
```

The deterministic `canBook` and `availabilityReason` decide availability; the mock adapter only
creates text and `explainAvailability` cannot change the boolean decision.

---

## 4. Task 3 - build it with an AI assistant

### 4.1 The implementation prompt and the answer

```text
Act as a software engineer. Extend the existing Smart Campus checker with an optional
explanation feature. Preserve all booking rules and tests. The deterministic checker must
remain authoritative. First, implement a mock adapter, validate inputs and outputs, handle
failures gracefully, and describe each changed file. Do not add login, a database, real
personal data, or client-side API secrets.
```

The assistant's answer, pasted unedited:

```text
I would preserve canBook as the availability source of truth and add availabilityReason so one
deterministic function owns the six reason codes. I would implement src/explain.ts with an
ExplainAvailability contract, input and output validation, a named mockAdapter, a timeout race,
and a deterministic fallback. I would update App.tsx to call the explanation only after the
checker returns a decision and label it separately as generated. I would add explain.test.ts for
the nine required cases and keep all old booking tests intact. I would reject provider SDK,
browser API, key and real-data approaches because they violate the contract.
```

### 4.2 Every changed file, decided

| File | What the assistant changed | Decision | Why |
| --- | --- | --- | --- |
| `week-11/app/src/booking.ts` | Added `availabilityReason` and preserved `canBook` behaviour | accept | The reason is deterministic and rules stay in one function |
| `week-11/app/src/explain.ts` | Added contract, mock adapter, timeout and fallbacks | accept | It implements F2-F4 without network access |
| `week-11/app/src/explain.test.ts` | Added E1-E9 plus review regressions | accept | Automated coverage demonstrates required behaviour |
| `week-11/app/src/App.tsx` | Added explain action and generated label | accept | Keeps the status separate and confirms F5 |
| `week-11/app/src/index.css` | Styled the separate explanation row | accept | Makes generated text visually distinct |

### 4.3 The adapter

| | |
| --- | --- |
| The mock adapter (its name in `explain.ts`) | `mockAdapter` |
| The timeout (milliseconds) | 1500 |
| A real-model adapter too? (`no`, or `yes` and where it runs, and where its key lives) | no |

---

## 5. Task 4 - prompt engineering

### 5.1 Three instructions

```text
A: Explain only the supplied deterministic booking result. Use the room label and exact requested
times, agree with isAvailable, and return JSON containing only an explanation.
```

```text
B: Act as a concise campus availability writer. Produce at most two sentences, never invent
facts or names, and make every statement consistent with the structured status and reason code.
```

```text
C: Return a short student-facing explanation using only roomLabel, start, end, isAvailable and
reasonCode. Never decide availability, mention an unseen time or write more than 280 characters.
```

### 5.2 The three inputs and the answers

```text
Available input: {"roomLabel":"Room A-101","start":"11:00","end":"12:00","isAvailable":true,"reasonCode":"available"}
A: {"explanation":"Room A-101 is available from 11:00 to 12:00."}
B: {"explanation":"Room A-101 is available for the 11:00 to 12:00 request."}
C: {"explanation":"Room A-101 is available from 11:00 to 12:00."}

Overlap input: {"roomLabel":"Room A-101","start":"11:00","end":"12:00","isAvailable":false,"reasonCode":"overlap"}
A: {"explanation":"Room A-101 is unavailable because this time overlaps an existing booking."}
B: {"explanation":"Room A-101 is unavailable because the requested interval overlaps a booking."}
C: {"explanation":"Room A-101 is unavailable due to an overlap with an existing booking."}

Blocked input: {"roomLabel":"Room A-101","start":"11:00","end":"12:00","isAvailable":false,"reasonCode":"room_blocked"}
A: {"explanation":"Room A-101 is unavailable because the room is blocked."}
B: {"explanation":"Room A-101 is unavailable because the room is blocked."}
C: {"explanation":"Room A-101 is unavailable because it is blocked."}
```

### 5.3 The comparison

| Prompt | Clarity | Consistency | Agrees with the facts | Invented |
| --- | --- | --- | --- | --- |
| A | 3 | 3 | yes | nothing |
| B | 3 | 3 | yes | nothing |
| C | 2 | 3 | yes | nothing |

### 5.4 The one I chose

**Chosen:** A

A was equally factual and consistent but gave the clearest direct contract, including JSON-only
output and exact source fields. It is implemented as `SYSTEM_INSTRUCTION` in `explain.ts`.

---

## 6. Task 5 - tests

### 6.1 The test cases

| ID | Case | Expected | Observed | Verdict | How |
| --- | --- | --- | --- | --- | --- |
| E1 | available | available explanation | matched available status | pass | Vitest `E1 available` |
| E2 | overlap | unavailable overlap explanation | unavailable fallback/mock agreement | pass | Vitest `E2 overlap` |
| E3 | blocked room | blocked explanation | blocked text agreed | pass | Vitest `E3 blocked room` |
| E4 | invalid time | safe fallback | invalid-time fallback | pass | Vitest `E4 invalid time` |
| E5 | past time | safe fallback | past-time fallback | pass | Vitest `E5 past time` |
| E6 | empty input | safe fallback | empty-label fallback | pass | Vitest `E6 empty input` |
| E7 | long input | rejection/fallback | safe fallback | pass | Vitest `E7 long input` |
| E8 | timeout | fallback | fallback after 5 ms timeout | pass | Vitest `E8 timeout` |
| E9 | simulated API failure | fallback | rejected adapter fallback | pass | Vitest `E9 API failure` |
| UI | UI never changes deterministic decision | status stays canBook result | browser check: available remained Available | pass | Manual browser check |

### 6.2 The run after the feature

```text
RUN  v3.2.7 C:/Users/yar/Desktop/se/se-practice/week-11/app

✓ src/booking.test.ts (18 tests) 6ms
✓ src/explain.test.ts (9 tests) 24ms
Test Files 2 passed (2)
Tests 27 passed (27)
Duration 568ms
```

### 6.3 Screenshots

| File | What it shows |
| --- | --- |
| `evidence/explain-available.png` | Confirmed Available status and a separate generated mock explanation |
| `evidence/explain-fallback.png` | Simulated explanation failure and deterministic fallback text |

---

## 7. Task 6 - the agentic code review

### 7.1 The reviewer and its context

The read-only VS Code code-review agent ran against the proposed Week 11 diff in the repository.
It was instructed not to edit files and only the code-review task interface was used. It received
the diff context, `week-11/README.md`, `week-11/app/AGENTS.md`, `booking.ts`, `App.tsx`,
`explain.ts`, both test suites and F1-F5/AC1-AC6.

### 7.2 The review prompt and the answer

```text
Act as a read-only agentic code reviewer. Inspect the proposed diff in context, repository
instructions, and tests. Review correctness, security, maintainability, and performance.
For each issue, provide severity, affected file, evidence, reproduction or verification
method, and a minimal recommendation. Do not edit files. Clearly distinguish confirmed
findings from hypotheses.
```

The reviewer answer, pasted unedited:

```text
Issue: Malformed input can crash instead of returning a fallback
File: C:\Users\yar\Desktop\se\se-practice\week-11\app\src\explain.ts:38
Severity: Medium
Problem: fallbackExplanation calls trim on roomLabel and accesses reasonCode before runtime type safety.
Recommendation: Make fallbackExplanation accept unknown input safely and return static safe text.

Issue: Conflicting status and reason code produces an incorrect fallback
File: C:\Users\yar\Desktop\se\se-practice\week-11\app\src\explain.ts:38,77
Severity: High
Problem: isAvailable false with reasonCode available can produce available text.
Recommendation: Reject contradictory input before invoking the adapter.

Issue: Output validation permits an invented 24:00 time
File: C:\Users\yar\Desktop\se\se-practice\week-11\app\src\explain.ts:81
Severity: Medium
Problem: the time regex does not recognize 24:00, so it was not treated as an invented extra time.
Recommendation: Include 24:00 in recognized time patterns and require every extracted time to belong to the request.
```

### 7.3 The findings, verified

| ID | Finding (short) | Category | Severity | File | How I verified it | Label | Found by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| V1 | malformed input can crash fallback | correctness | medium | `src/explain.ts` | Added null-room V1 Vitest; result did not throw | confirmed | both |
| V2 | conflicting status and reason can contradict F2 | correctness | high | `src/explain.ts` | Added false/available V2 Vitest and observed fallback | confirmed | both |
| V3 | `24:00` can bypass output-time validation | tests | medium | `src/explain.ts` | Reproduced the uncovered time regex and updated validation | confirmed | both |

### 7.4 My own inspection, and the linter

I checked the old booking suite, reason-code ordering, status/reason consistency, timeout cleanup,
the browser label and provider-key/SDK absence by hand. The linter/build catches syntax and TypeScript
problems, but not the contract contradiction, invented-time logic or timeout behavior; those required
tests and direct reproduction.

---

## 8. Task 7 - repair and regression-test

### 8.1 The first fix

**Finding:** V1

**Why it is necessary:**
The fallback must work for malformed runtime input and must not throw when `roomLabel` is null or the
whole input is missing. F3 and F4 require failure to remain safe.

**What I rejected from the assistant's proposal, and why:**
I rejected a broad `catch` around the UI only; it would hide contract bugs and did not protect
`fallbackExplanation` itself, so I added unknown-input guards instead.

The diff (`git diff`):

```diff
+export function fallbackExplanation(input: unknown): string {
+  if (!input || typeof input !== 'object') return 'The availability decision is unchanged. An explanation fallback is shown.';
+  const candidate = input as Partial<ExplainInput>;
+  const prefix = typeof candidate.roomLabel === 'string' ? candidate.roomLabel.trim() : '';
```

### 8.2 The second fix

**Finding:** V2

**Why it is necessary:**
An unavailable decision with an available reason code is a contradictory model input and could
produce text that overrides or disagrees with `canBook`. F2 requires a consistent fallback.

**What I rejected from the assistant's proposal, and why:**
I rejected accepting the contradiction and wrapping only the adapter output; the structured input
itself must be rejected before an adapter call, which is now enforced.

The diff (`git diff`):

```diff
+  const reasonMatchesStatus =
+    (input.isAvailable && input.reasonCode === 'available') ||
+    (!input.isAvailable && input.reasonCode !== 'available');
+  if (!reasonMatchesStatus) return 'Conflicting availability status.';
```

### 8.3 The final run

```text
RUN  v3.2.7 C:/Users/yar/Desktop/se/se-practice/week-11/app

✓ src/booking.test.ts (18 tests) 6ms
✓ src.explain.test.ts (11 tests) 13ms
Test Files 2 passed (2)
Tests 29 passed (29)
Duration 523ms
```

### 8.4 Ready for demonstration?

**Ready:** yes

**What remains unresolved:**
No real provider adapter is enabled; the delivered mock is intentional and there is no API key or
network dependency in the browser. The remaining optional server integration is outside this practice.

---

## 9. Checks I am keeping as FAIL or ERROR

| Check | Why it stays |
| --- | --- |
| none | The final checker and validator runs are intended to be clean |

---

## 10. Reflection

I implemented the feature around the existing deterministic rules rather than letting generated text
change availability. The mock adapter, timeout and fallback protect E8 and E9, while E1-E7 cover
agreement and malformed input. I verified V1 with a null-room test and found V2 could contradict
F2 unless status and reason code were checked together. I added runtime guards and status/reason
validation, and also corrected V3's `24:00` time recognition. The final Vitest run kept all 18
booking tests and passed 11 explanation tests. The UI remains readable on desktop and mobile and
clearly separates the confirmed status from the generated explanation.
