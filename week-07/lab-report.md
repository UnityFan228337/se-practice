# Week 07 — Lab report

**Name:** Yaroslav
**Group:** not provided
**Date:** 2026-11-04

Fill in every section. **Do not delete, rename or renumber the headings.** The checker and the
grader find your answers by them. You can add rows to any table, but never remove its header.

---

## 1. Setup

| | |
| --- | --- |
| Project I continue (`week-06` = my Week 06 Bolt project, `starter` = the provided starter) | `starter` |
| Bolt project link (or `not shared`, and why) | `not shared` — this submission uses the provided starter, not a Bolt project. |
| Assistant that generated the tests (tool) | Copilot SDK in VS Code |
| Exact model (with its version, or `not displayed`) | not displayed |
| Where I ran the tests (Bolt terminal / my computer / Codespace) | My computer (Windows; Node.js v26.13.0) |
| Vitest version (the `RUN  v…` line of a run) | 3.2.7 |
| Test command | `npm test` (runs `vitest run` in `app/`) |

---

## 2. Task 1 — baseline and the booking function

**Before editing:** where did the booking decision live in the project you started from?

| | |
| --- | --- |
| File and function (or "inside the page component") | `starter/src/App.tsx`, inside `check()` |
| Its inputs | Start, end and current time converted to minutes; the blocked flag; the selected room's bookings |
| What it returned | A boolean decision stored as the page's result |
| How the page used it | `check()` set the result to Available or Unavailable after evaluating the booking rules |

**What I changed to extract `canBook`.** Say which file it now lives in, what you moved, and why
the behaviour did not change. Also say which file of the page now calls it. 40 words or more.

<!-- Write below this line -->

I moved the existing interval, current-time, duration, blocked-room, and overlap conditions from `check()` in `App.tsx` into `app/src/booking.ts` as `canBook`. The component still converts time inputs and shows the same validation message, then passes those values and the selected room's bookings to the extracted function. I preserved the original conditions and ordering; the page now calls `canBook` for its decision. I checked the extraction against the starter source and exercised it with the fixed test cases; no booking data is mutated by the function.

---

## 3. Task 2 — the test plan

Default fixture: `now = 540`, `blocked = false`, `bookings = [{ start: 600, end: 660 }]`, fresh
for every test. **The Expected column comes from AC1–AC4, never from the code.** Write the
**reason** for each expected result **before** you send the generation prompt.

| ID | Candidate / changed input | Expected | AC | Reason (in your words) |
| --- | --- | --- | --- | --- |
| T01 | 660–720 (touching after) | true | AC4 | The candidate starts exactly when the existing booking ends, so the intervals do not overlap. |
| T02 | 540–570 (starts now) | false | AC1 | The start equals now, but AC1 requires the start to be strictly later. |
| T03 | 720–720 (zero duration) | false | AC1 | Start and end are equal, so the interval is not positive in length. |
| T04 | 750–720 (reversed) | false | AC1 | The start is later than the end, violating start < end. |
| T05 | 1380–1441 (past day end) | false | AC1 | The end exceeds 1440, the latest permitted endpoint. |
| T06 | 720–840 (120 minutes) | true | AC2 | The duration equals the limit; AC2 rejects only durations longer than 120 minutes. |
| T07 | 720–841 (121 minutes) | false | AC2 | The duration is 121 minutes, which is longer than the permitted maximum. |
| T08 | 570–600 (touching before) | true | AC4 | The candidate ends exactly when the existing booking starts; touching is allowed. |
| T09 | 630–690 (partial overlap) | false | AC4 | The intervals share the 630–660 time range. |
| T10 | 570–690 (contains booking) | false | AC4 | The candidate includes the entire existing booking. |
| T11 | 615–645 (inside booking) | false | AC4 | The candidate lies completely inside the existing booking. |
| T12 | 600–660 (identical interval) | false | AC4 | The candidate covers exactly the same interval as the existing booking. |
| T13 | 660–720, blocked = true | false | AC3 | The interval is otherwise valid, but the selected room is blocked. |
| T14 | 630–690, bookings = [] | true | AC4 | With no existing bookings, there is nothing for this valid request to overlap. |
| AC5 | an Available request — the bookings after the call equal the bookings before | true, data unchanged | AC5 | Check an available candidate and compare the booking array to its pre-call copy. |
| X1 | 1380–1440 (ends exactly at day end) | true | AC1 | 1440 is an allowed inclusive upper bound, and the request is after now and within 120 minutes. |
| X2 | 690–730 with bookings 600–660 and 720–780 | false | AC4 | The candidate overlaps the second booking from 720 to 730, even though it misses the first. |

X1 and X2 are **your own two cases**: a boundary or a state that T01–T14 do not reach. Fill all
five columns.

---

## 4. Task 3 — the generation prompt and the first suite

**The deck's generation prompt used as the test specification.** It was not sent as a separate,
verbatim message; the tests were generated in this Copilot conversation:

```text
Generate tests for the existing booking function using Vitest. Use AC1–AC6 and the reviewed case table below.

Import the real function used by the page. Keep its code unchanged. Use fixed time and fresh fixtures. Assert exact decisions and unchanged booking data.

Return test file, run command, and AC mapping. Flag unclear requirements. We will run the tests ourselves.

Case table:
| ID | Candidate / changed input | Expected | AC | Reason |
| T01 | 660–720 (touching after) | true | AC4 | The intervals only touch. |
| T02 | 540–570 (starts now) | false | AC1 | Start must be after now, not equal to it. |
| T03 | 720–720 (zero duration) | false | AC1 | Start must be less than end. |
| T04 | 750–720 (reversed) | false | AC1 | Start must be less than end. |
| T05 | 1380–1441 (past day end) | false | AC1 | End must not exceed 1440. |
| T06 | 720–840 (120 minutes) | true | AC2 | AC2 rejects only durations longer than 120 minutes. |
| T07 | 720–841 (121 minutes) | false | AC2 | The duration exceeds 120 minutes. |
| T08 | 570–600 (touching before) | true | AC4 | The intervals only touch. |
| T09 | 630–690 (partial overlap) | false | AC4 | The candidate overlaps the existing interval. |
| T10 | 570–690 (contains booking) | false | AC4 | The candidate contains the existing interval. |
| T11 | 615–645 (inside booking) | false | AC4 | The candidate is inside the existing interval. |
| T12 | 600–660 (identical interval) | false | AC4 | The intervals are identical and overlap. |
| T13 | 660–720, blocked = true | false | AC3 | The selected room is blocked. |
| T14 | 630–690, bookings = [] | true | AC4 | There is no existing booking to overlap. |
| AC5 | Available request; compare bookings before and after | true, data unchanged | AC5 | Existing booking data must not change. |
| X1 | 1380–1440 (ends exactly at day end) | true | AC1 | 1440 is the permitted boundary. |
| X2 | 690–730 with bookings 600–660 and 720–780 | false | AC4 | The candidate overlaps the second booking. |
```

**Summary of the assistant's output** (not a verbatim transcript): run command, AC mapping and
unclear requirement. Its first test file is in `suites/first/`:

```text
Run command: `npm test` from `app/`.
AC mapping: T01, T08, T09–T12, T14 and X2 cover AC4; T02–T05 and X1 cover AC1;
T06–T07 cover AC2; T13 covers AC3; the AC5 test compares the bookings before and after
an available request. The suite imports the real `canBook` and uses fixed inputs.
Unclear requirement: AC1–AC4 do not specify how an invalid existing booking should be handled.
The first generated suite incorrectly expected a 120-minute request to be rejected; this is
reviewed and corrected in the final suite.
```

The first suite was saved to `suites/first/` **before** I changed anything in it: yes

---

## 5. Task 4 — review of the first suite

Review it **before** you run it. Look at the imports, the expected values, isolation, duplicates
and skipped tests. Make one row per decision. At least **two** rows, and each one names the kind of
weakness (the deck's table: *no exception occurred* · *expected = current output* · *only valid
requests* · *mocked booking function*, or your own) and the AC that decides it.

| # | Test or part of the suite | What is weak or wrong | Decision: accept / revise / reject | AC or reason |
| --- | --- | --- | --- | --- |
| 1 | T06 expected result | It expected exactly 120 minutes to be rejected, contradicting AC2, which rejects only durations longer than 120 minutes. | revise | AC2: preserve the expected `true` value; do not change the implementation to satisfy the bad expectation. |
| 2 | Imports and assertions | It imports the real `canBook`, uses fixed fixtures, and asserts exact booleans. The AC5 test compares the bookings with a saved copy. | accept | The tests exercise the same function called by the page and verify AC5 data preservation. |

---

## 6. Task 5 — running, diagnosing, improving

### 6.1 The first run

The **real** terminal output of the first run of the first suite, pasted unedited. Include the
`RUN  v…` line and the `Tests` summary line. A build message or the assistant saying "tests pass"
is not a run.

```text
 RUN  v3.2.7 C:/Users/yar/Desktop/se/se-practice/week-07/app

 ❯ src/booking.test.ts (17 tests | 1 failed) 10ms
   ✓ canBook > T01 AC4: touching after an existing booking is allowed 1ms
   ✓ canBook > T02 AC1: a request starting at the current time is rejected 0ms
   ✓ canBook > T03 AC1: a zero-duration request is rejected 0ms
   ✓ canBook > T04 AC1: a reversed request is rejected 0ms
   ✓ canBook > T05 AC1: a request ending after 24:00 is rejected 0ms
   × canBook > T06 AC2: exactly 120 minutes is rejected 7ms
     → expected true to be false // Object.is equality
   ✓ canBook > T07 AC2: a 121-minute request is rejected 0ms
   ✓ canBook > T08 AC4: touching before an existing booking is allowed 0ms
   ✓ canBook > T09 AC4: a partial overlap is rejected 0ms
   ✓ canBook > T10 AC4: a request containing an existing booking is rejected 0ms
   ✓ canBook > T11 AC4: a request inside an existing booking is rejected 0ms
   ✓ canBook > T12 AC4: an identical interval is rejected 0ms
   ✓ canBook > T13 AC3: a blocked room is rejected 0ms
   ✓ canBook > T14 AC4: a request is allowed when there are no existing bookings 0ms
   ✓ canBook > AC5: an available request does not change existing booking data 0ms
   ✓ canBook > X1 AC1: ending exactly at 24:00 is allowed 0ms
   ✓ canBook > X2 AC4: overlap with the second of multiple bookings is rejected 0ms

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ Failed Tests 1 ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

 FAIL  src/booking.test.ts > canBook > T06 AC2: exactly 120 minutes is rejected
AssertionError: expected true to be false // Object.is equality

- Expected
+ Received

- false
+ true

 ❯ src/booking.test.ts:32:61
     30| 
     31|   test('T06 AC2: exactly 120 minutes is rejected', () => {
     32|     expect(canBook({ ...fixture(), start: 720, end: 840 })).toBe(false…
       |                                                             ^
     33|   });
     34| 

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/1]⎯

 Test Files  1 failed (1)
      Tests  1 failed | 16 passed (17)
   Start at  16:50:32
   Duration  408ms (transform 32ms, setup 0ms, collect 32ms, tests 10ms, environment 0ms, prepare 97ms)
```

**Each failure, diagnosed** (the deck's table: import/runner error · assertion mismatch · result
changing per run · no tests discovered). Write `none` in the first row if nothing failed.

| Failing test | Observed failure | First check | Test repair or implementation fix? | Action taken |
| --- | --- | --- | --- | --- |
| T06 AC2 | Expected `false`, received `true` for a 120-minute request | Compare the expected value with AC2: only durations greater than 120 are rejected. | Test repair | Corrected the final-suite expectation and title to `true` / allowed. The implementation's `> 120` condition matches AC2. |

### 6.2 The improvement prompt

The deck's improvement prompt is recorded below. It was not sent as a separate, verbatim message;
the review followed the actual output from 6.1 in this conversation:

```text
Review this test suite against AC1–AC6 and our case table. Identify incorrect expectations, weak assertions, duplicated cases, and missing boundaries.

For each proposed change, explain the requirement and the defect it could detect. Improve the tests without changing correct expectations to match buggy behavior.

Use the actual failure output below. Separate test repairs from implementation fixes.

Actual first-run result: `Tests  1 failed | 16 passed (17)`.
Failure: T06 expected `false` but received `true` for start=720, end=840. AC2 says to reject bookings longer than 120 minutes, so exactly 120 minutes is valid.

Assistant review: Revise only T06's expected result and title to say that exactly 120 minutes is allowed. Do not change `canBook`: its `end - start > 120` check implements AC2. The remaining cases use exact boolean assertions, fresh fixed fixtures, the real function, an AC5 before/after comparison, and the X1/X2 boundaries. Keep the final suite at 17 tests.
```

### 6.3 The final run

The **real** output of the final suite (`booking.test.*` beside your module), after every
change and after restoring the correct code from section 7. Every test must pass. If a real defect
is still open, leave its test failing and explain it in 9.1.

```text
> smart-campus-availability@0.0.0 test
> vitest run

 RUN  v3.2.7 C:/Users/yar/Desktop/se/se-practice/week-07/app

 ✓ src/booking.test.ts (17 tests) 3ms

 Test Files  1 passed (1)
      Tests  17 passed (17)
   Start at  17:17:23
   Duration  468ms (transform 32ms, setup 0ms, collect 33ms, tests 3ms, environment 0ms, prepare 123ms)
```

---

## 7. Task 6 — deliberate defects

You need a reviewed, passing suite first. Then introduce **one** defect at a time in your booking
module, leave the tests unchanged, run, record, and **restore** the code. A syntax or import
error does not count as detection.

| Trial | Intentional change | Detected / Survived | Failing test ID(s) | If it survived: why, and what you added |
| --- | --- | --- | --- | --- |
| M1 | Reject duration >= 120 instead of > 120 | Detected | T06 | |
| M2 | Treat touching endpoints as an overlap | Detected | T01, T08 | Both endpoint tests fail when touching is incorrectly considered overlap. |
| M3 | Remove the blocked-room rejection | Detected | T13 | The blocked-room test fails when the rejection is removed. |

**The run of each mutant, pasted unedited.** Paste the `Tests` summary line and the failing test
names at least:

```text
M1 (actual run):
× canBook > T06 AC2: exactly 120 minutes is allowed
Tests  1 failed | 16 passed (17)

M2 (actual run):
× canBook > T01 AC4: touching after an existing booking is allowed
× canBook > T08 AC4: touching before an existing booking is allowed
× canBook > AC5: an available request does not change existing booking data
Tests  3 failed | 14 passed (17)

M3 (actual run):
× canBook > T13 AC3: a blocked room is rejected
Tests  1 failed | 16 passed (17)
```

All three mutants were restored before the passing final run.

---

## 8. Task 7 — manual UI checks

Use `now = 09:00` and an existing `10:00–11:00` booking. Do them in the page in a browser. Save a
screenshot of each as `evidence/ui-1.png` … `evidence/ui-5.png`. Take **ui-4 at phone width**
(about 375 px, portrait).

| # | Action | Expected observation | AC | What I observed | Pass / Fail / Not testable |
| --- | --- | --- | --- | --- | --- |
| U1 | Check 11:00–12:00, unblocked | Available, with the fixed sample booking | AC5 | The page showed Available and the existing 10:00–11:00 booking. Screenshot: `evidence/ui-1.png`. | Pass |
| U2 | Enable blocked, then check again | Unavailable replaces the earlier result | AC3, AC5 | After enabling Room blocked, the result changed to Unavailable. Screenshot: `evidence/ui-2.png`. | Pass |
| U3 | Clear a required input and submit | Understandable validation feedback | AC6 | Clearing Start and submitting showed “Fill in the current time, the start and the end.” Screenshot: `evidence/ui-3.png`. | Pass |
| U4 | Use a narrow (phone) width | Controls and result remain usable | AC6 | At 375 px viewport width, controls stacked vertically and the result remained visible. Screenshot: `evidence/ui-4.png` (portrait). | Pass |
| U5 | Repeat the checks on the same data | Existing bookings remain unchanged | AC5 | Repeated the available check; the displayed existing booking remained 10:00–11:00. Screenshot: `evidence/ui-5.png`. | Pass |

---

## 9. Comparison and what still fails

### 9.1 Checks I am keeping as FAIL or ERROR

Use the same IDs as `known_fails` in `submission.yml`. Write `none` if the run is clean.

| Check | Why it stays |
| --- | --- |
| none | All 33 checker checks pass; no failures are being kept. |

### 9.2 Original and improved suites

| Measure | First suite | Improved suite |
| --- | --- | --- |
| Executed / passed / failed | 17 / 16 / 1 | 17 / 17 / 0 |
| Requirements with meaningful tests (AC IDs and gaps) | T01–T14 plus AC5, X1, X2; AC1–AC5 represented. AC6 was not tested in the first suite. | T01–T14 plus AC5, X1, X2; AC1–AC5 unit-tested and AC6 checked manually. |
| Selected mutants detected | M1 detected by T06; M2 and M3 not yet tried | M1/T06, M2/T01 and T08, M3/T13 |
| Accepted / revised / rejected tests | Accepted: suite structure, exact assertions and real import; revised: T06 expected value | Accepted tests retained; T06 corrected to match AC2. |
| Remaining limitations | M2/M3 and UI behavior/screenshots had not yet been checked. | Unit tests cover selected fixed inputs; behavior for malformed existing bookings is not specified by the ACs. |

### 9.3 What no AC decides

Call your function with `bookings = [{ start: 700, end: 650 }]` (a reversed existing booking)
and a request of 660–720. What does it return? Does any AC say what it should return? (This is
the value you declare in `submission.yml` under `assumptions.invalid_existing_booking`.)

For `bookings = [{ start: 700, end: 650 }]` and a request of 660–720, the function returns `true`: neither overlap comparison is true for the reversed interval. No AC specifies how invalid existing bookings should be handled, so this is an implementation assumption, not an AC requirement.

---

## 10. Conclusion (120–180 words)

<!-- Answer all three in your own words, without the assistant:
     (a) Which mistake in the FIRST suite would have let a wrong canBook pass, and how did you find it?
     (b) What does your final green run prove, and what does it NOT prove? Use a mutant or a UI check.
     (c) One testing limitation that remains.
     Worthless: "The AI wrote good tests and they all passed."
     Worth everything: "The first suite expected T06 (exactly 120 minutes) to be rejected. That
     contradicts AC2, and it failed on a correct canBook. If I had changed the code to make it
     pass, M1 would have become the real behaviour." -->

<!-- Write your conclusion below this line -->
The first suite's T06 expected a 120-minute request to be rejected. I checked that against AC2, which rejects bookings only when they are longer than 120 minutes, and ran the suite: T06 failed against the correct rule. Changing the function to satisfy that test would incorrectly reject a valid booking. In the corrected suite, T06 expects exactly 120 minutes to be allowed. The final run passes all 17 tests for their fixed inputs, including interval boundaries, blocked rooms, overlaps, booking-data preservation and the two extra cases. It does not prove that the page works in a browser or at phone width, and it cannot cover every possible interval. M1 was detected by T06; M2 and M3 were not run, so their detection remains unverified. The manual UI checks and screenshots are also missing. Another limitation is that no acceptance criterion defines what to do with malformed existing bookings. The current function returns true for a reversed existing booking, but that behavior needs a product decision.

*AI-assisted draft; Yaroslav should review and personalize this conclusion before submission.*
