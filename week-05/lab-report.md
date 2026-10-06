# Week 05 — Lab report

**Name:** Ярослав
**Group:**  [CSCI-2208] Software Engineering - Fall 2026
**Date:** 10.06

Fill in every section. **Do not delete, rename or renumber the headings** — the checker and the
grader find your answers by them. Add rows to any table; never remove its header.

---

## 1. Setup

## 1. Setup
 
| | |
| --- | --- |
| Assistant (tool) | Claude (claude.ai) |
| **Exact** model name | Claude Sonnet 5.5 |
| Language and version | Python 3 (standard library only; the grader runs 3.13) |
| Path | A |
| My Week 04 declaration for touching bookings | allowed |

<!-- If your Week 04 model said touching bookings are NOT allowed: AC4 now says they are.
     One sentence here on what that changes in your Week 04 diagrams. This is a finding, not a penalty. -->

---

## 2. Task 1 — the plan

**The assistant's plan, pasted unedited:**

```text
Implementation plan for can_book(start, end, now, blocked, existing)
 
Checks, in order. Each one returns False immediately; if none fires, return True.
 
1. Day bounds and order (AC1): require 0 <= start < end <= 1440.
2. Future start (AC1): require start > now.
3. Duration (AC2): require end - start <= 120.
4. Blocked room (AC3): if blocked is True, return False.
5. Overlap (AC4): for every (b_start, b_end) in existing, the new interval
   overlaps it when start < b_end and b_start < end. If any booking overlaps,
   return False. Touching endpoints are not an overlap, because the end is excluded.
6. Otherwise return True (AC5). Only read existing; never sort, append or remove.
 
Assumptions
- The inputs are valid as the contract states (integers, now in 0-1439,
  existing holds valid tuples), so no extra input validation is needed.
- existing may be unsorted, so every booking is examined instead of stopping early.
- The result is the Boolean True or False, never None, 0/1 or a string.
 
Boundary cases that could expose an incorrect implementation
- (660, 720) against (600, 660): touching at the existing end -> True
- (570, 600) against (600, 660): touching at the existing start -> True
- (630, 690), (570, 630), (615, 645), (570, 690), (600, 660): every overlap shape -> False
- duration exactly 120 -> True; 121 -> False
- start == now -> False; start == now + 1 -> True
- start == end (zero length) and start > end (reversed) -> False
- end == 1440 -> True; end == 1441 -> False
- start == 0 with now == 0 -> False
- blocked room with an otherwise valid request -> False
- empty existing; several bookings where only the second or the last one overlaps
- an unsorted existing list is the same list, in the same order, after the call
```
 
**What the plan invented or changed.** One row for every rule in the plan that is not in the
contract or in AC1–AC5, or that says something different from them. If you found none, write one
row saying which lines of the plan you checked against which AC.
 
| # | What the plan said | What the contract or the AC says | What I did |
| --- | --- | --- | --- |
| 1 | I found no invented rule. I checked steps 1–2 against AC1, step 3 against AC2, step 4 against AC3, step 5 against AC4 (strict `<` on both sides because "intervals include the start and exclude the end"), step 6 against AC5 and "Keep all inputs unchanged". | The three assumptions restate the contract ("valid", "Return True or False"); none adds a gap between bookings, a sort, a stored booking or an input check. | Nothing to drop. I did not need to tell the assistant to remove a step. The one decision the plan leaves to me is what happens for a non-integer time (report 9.2). |
 
**Boundary cases the assistant suggested that I kept as tests:**
 
- touching at the existing end (660, 720) and at the existing start (570, 600)
- all five overlap shapes: partial both sides, inside, containing, identical
- duration 120 (allowed) and 121 (rejected)
- start == now and start == now + 1; start 0 with now 0
- zero-length, reversed, end == 1440, end == 1441
- blocked room, empty `existing`, overlap only with the second booking
- an unsorted `existing` is unchanged after the call
---

## 3. Task 2 — the first version (v1), read before it was run

v1 is saved as `code/original/booking_v1.py`, exactly as the assistant returned it: yes
 
**AC map.** One row per condition in v1. Quote the line.
 
| # | Line in v1 | AC it implements | Correct as written? If not, why |
| --- | --- | --- | --- |
| 1 | `if not (0 <= start < end <= 1440): return False` | AC1 (order and day bounds) | Correct. `start < end` rejects zero-length and reversed; `end <= 1440` allows 1440; `0 <= start` is the lower bound. |
| 2 | `if start <= now: return False` | AC1 (`start > now`) | Correct. `<=` is right here: starting exactly now is rejected. |
| 3 | `if end - start > 120: return False` | AC2 | Correct. Strict `>` keeps exactly 120 minutes allowed. |
| 4 | `if blocked: return False` | AC3 | Correct. Rejects any request for a blocked room. |
| 5 | `if start < booked_end and booked_start < end: return False` (inside `for booked_start, booked_end in existing`) | AC4 | Correct. Both comparisons are strict, so touching endpoints are not an overlap; the loop looks at every booking and does not assume a sorted list. |
| 6 | `return True` | AC5 | Correct. Reached only when every check above passed; the literal `True` is a real Boolean, and `existing` was only read. |
 
**Anything in v1 that no AC asks for** (extra validation, a buffer between bookings, logging,
saving the booking, a different return type):
 
- Nothing. v1 has no input validation, no buffer, no sorting, no logging, no saving.
- Reading it against the ACs, the risky points were: `>` against `>=` at 120 minutes, `start <= now`, and the two strict comparisons in the overlap line. All four are as AC1, AC2 and AC4 require.
---

## 4. Task 3 — my tests
 
Base input for every row unless the row says otherwise: `now=540, blocked=False, existing=[(600, 660)]`.
 
| # | Test name | Request (start, end) | What differs from the base input | Expected | AC | Result on v1 | Result on final |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `test_touching_end_is_allowed` | (660, 720) | — | True | AC4 | ok | ok |
| 2 | `test_overlap_is_rejected` | (630, 690) | — | False | AC4 | ok | ok |
| 3 | `test_blocked_room_is_rejected` | (660, 720) | blocked=True | False | AC3 | ok | ok |
| 4 | `test_exactly_two_hours_is_allowed` | (720, 840) | — | True | AC2 | ok | ok |
| 5 | `test_over_two_hours_is_rejected` | (720, 841) | — | False | AC2 | ok | ok |
| 6 | `test_starting_now_is_rejected` | (540, 570) | — | False | AC1 | ok | ok |
| 7 | `test_one_minute_after_now_is_allowed` | (541, 571) | — | True | AC1 | ok | ok |
| 8 | `test_start_in_the_past_is_rejected` | (500, 530) | — | False | AC1 | ok | ok |
| 9 | `test_now_zero_start_zero_is_rejected` | (0, 60) | now=0, existing=[] | False | AC1 | ok | ok |
| 10 | `test_now_zero_start_one_is_allowed` | (1, 61) | now=0, existing=[] | True | AC1 | ok | ok |
| 11 | `test_zero_length_is_rejected` | (700, 700) | — | False | AC1 | ok | ok |
| 12 | `test_reversed_times_are_rejected` | (720, 700) | — | False | AC1 | ok | ok |
| 13 | `test_end_exactly_at_midnight_is_allowed` | (1380, 1440) | existing=[] | True | AC1 | ok | ok |
| 14 | `test_end_after_midnight_is_rejected` | (1380, 1441) | existing=[] | False | AC1 | ok | ok |
| 15 | `test_negative_start_is_rejected` | (-30, 30) | now=0, existing=[] | False | AC1 | ok | ok |
| 16 | `test_last_minute_of_the_day_is_allowed` | (1439, 1440) | now=1438, existing=[] | True | AC1 | ok | ok |
| 17 | `test_one_minute_booking_is_allowed` | (720, 721) | — | True | AC2 | ok | ok |
| 18 | `test_blocked_room_with_no_bookings_is_rejected` | (660, 720) | blocked=True, existing=[] | False | AC3 | ok | ok |
| 19 | `test_overlap_over_the_start_is_rejected` | (570, 630) | — | False | AC4 | ok | ok |
| 20 | `test_inside_existing_booking_is_rejected` | (615, 645) | — | False | AC4 | ok | ok |
| 21 | `test_containing_existing_booking_is_rejected` | (570, 690) | — | False | AC4 | ok | ok |
| 22 | `test_identical_to_existing_booking_is_rejected` | (600, 660) | — | False | AC4 | ok | ok |
| 23 | `test_ending_at_existing_start_is_allowed` | (570, 600) | — | True | AC4 | ok | ok |
| 24 | `test_empty_existing_is_allowed` | (600, 660) | existing=[] | True | AC4 | ok | ok |
| 25 | `test_overlap_with_second_booking_is_rejected` | (720, 780) | existing=[(600, 660), (700, 760)] | False | AC4 | ok | ok |
| 26 | `test_overlap_in_unsorted_list_is_rejected` | (610, 650) | existing=[(900, 960), (600, 660)] | False | AC4 | ok | ok |
| 27 | `test_fits_exactly_between_two_bookings` | (660, 720) | existing=[(600, 660), (720, 780)] | True | AC4 | ok | ok |
| 28 | `test_free_slot_among_three_bookings` | (760, 800) | existing=[(600, 660), (700, 760), (800, 860)] | True | AC4 | ok | ok |
| 29 | `test_existing_unchanged_after_accepted_request` | (780, 840) | existing=[(900, 960), (600, 660), (700, 760)]; list compared with a copy | True | AC5 | ok | ok |
| 30 | `test_existing_unchanged_after_rejected_request` | (610, 650) | existing=[(900, 960), (600, 660), (700, 760)]; list compared with a copy | False | AC5 | ok | ok |
| 31 | `test_existing_unchanged_when_blocked` | (780, 840) | blocked=True, existing=[(900, 960), (600, 660)]; list compared with a copy | False | AC5 | ok | ok |
| 32 | `test_result_is_a_boolean_in_every_branch` | five requests, one per branch | accepted / overlap / blocked / too long / reversed | bool each time | AC5 | ok | ok |
| 33 | `test_non_integer_time_is_not_handled_but_still_returns_a_boolean` | (600.5, 660.5) | existing=[] | a bool (decision of report 9.2; not in AC1–AC5) | none (§9.2) | ok | ok |
 
All 33 tests ran on v1 and on the final version; every one is green on both. Each request is chosen so that exactly one rule decides it (for example `(700, 700)` is far from the booking and short enough, so only `start < end` can reject it).
 
---
 
## 5. Task 4 — debugging with evidence
 
One row per defect you found — in v1, in a later version, or in your own tests. If v1 passed
everything, the row is the **new edge case you added**, with expected and actual equal, and the
cause column says why no change was needed.
 
| # | Input (the full call) | Expected | Actual | Cause (quote the line) | Fix | Who proposed the fix |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `can_book(1439, 1440, 1438, False, [])` — the new edge case `test_last_minute_of_the_day_is_allowed` | `True` (AC1: `0 <= 1439 < 1440 <= 1440` and `1439 > 1438`; 1 minute; not blocked; no bookings) | `True` | No defect. `if not (0 <= start < end <= 1440)` accepts `end == 1440`, and `if start <= now` is `1439 <= 1438`, which is false. | none — v1 passed all 33 tests and F1–F10, so there was nothing to fix | n/a (edge case chosen by me) |
 
**The debug prompt I sent, and the assistant's answer** (leave the block empty if you did not use it):
 
```text
```
 
---
 
## 6. Task 5 — the critique
 
**The assistant's critique, pasted unedited:**
 
```text
1. `if not (0 <= start < end <= 1440):` — nothing checks that start and end are
   integers (a float or string would be accepted or crash). Concerns the contract
   line "Times are integers", and AC1.
2. `for booked_start, booked_end in existing:` — every entry is assumed to be a
   2-tuple; a malformed entry raises ValueError. Concerns the contract line
   "existing contains valid (start, end) tuples".
3. `if start <= now:` — `now` is not checked to be in 0-1439. Concerns the contract
   line "now is valid (0-1439)".
4. `if blocked:` — this tests truthiness, so a non-Boolean such as the string
   "False" would count as blocked. Concerns the contract line "blocked is a Boolean"
   and AC3.
5. The docstring says what the function returns but not that `existing` is left
   untouched; the only mention of AC5 is the comment before the final `return True`.
   Concerns AC5 "never alter existing".
```
 
| # | Suggestion | accept / reject | Reason — cite the AC or the contract line | Suite after the change |
| --- | --- | --- | --- | --- |
| 1 | Check that start and end are integers | reject | The contract states "Times are integers", so the caller guarantees it; AC5 also says to return False, and a new check or exception is a rule that neither the contract nor AC1–AC5 asks for. See report 9.2. | no change made; 33 tests OK |
| 2 | Validate the entries of `existing` | reject | The contract says `existing` "contains valid (start, end) tuples for this room's active bookings only". Validating it adds scope beyond "Keep the feature within the stated scope". | no change made; 33 tests OK |
| 3 | Check that `now` is in 0-1439 | reject | The contract says "now is valid (0-1439)". Re-checking a guaranteed input is an invented rule. | no change made; 33 tests OK |
| 4 | Use `blocked is True` instead of `if blocked:` | reject | The contract says "blocked is a Boolean", so truthiness and `is True` give the same result for every allowed input; AC3 asks for nothing more. | no change made; 33 tests OK |
| 5 | State in the docstring that `existing` is never modified | accept | AC5 and the contract line "Keep all inputs unchanged" say so; a comment-only change, no behaviour moves. I added one docstring line. | 33 tests OK; checker F1–F10 still PASS |
 
---
 
## 7. Change log — v1 to final
 
| # | What changed (the line, before → after) | Why | Evidence: the test or check that moved |
| --- | --- | --- | --- |
| 1 | Docstring only: added the line `The list \`existing\` is only read, never modified (AC5).` after the line about touching intervals; no executable line changed (`diff` of `code/original/booking_v1.py` and `code/booking.py` shows only this added line). | Critique point 5: the contract says "Keep all inputs unchanged" and AC5 says "never alter existing", and v1's docstring did not say it. | Nothing moved: the suite is 33 OK before and after, F1–F10 PASS before and after. The checker reports "identical to your final: no" only because of this docstring line. No behavioural change was needed — v1 passed everything, see report 5. |
 
---
 
## 8. Evidence — real output
 
### 8.1 My suite, final run
 
Paste the **complete** terminal output. For Python: everything `python -m unittest -v` printed.
 
```text
test_blocked_room_is_rejected (test_booking.BookingTests.test_blocked_room_is_rejected) ... ok
test_blocked_room_with_no_bookings_is_rejected (test_booking.BookingTests.test_blocked_room_with_no_bookings_is_rejected) ... ok
test_containing_existing_booking_is_rejected (test_booking.BookingTests.test_containing_existing_booking_is_rejected) ... ok
test_empty_existing_is_allowed (test_booking.BookingTests.test_empty_existing_is_allowed) ... ok
test_end_after_midnight_is_rejected (test_booking.BookingTests.test_end_after_midnight_is_rejected) ... ok
test_end_exactly_at_midnight_is_allowed (test_booking.BookingTests.test_end_exactly_at_midnight_is_allowed) ... ok
test_ending_at_existing_start_is_allowed (test_booking.BookingTests.test_ending_at_existing_start_is_allowed) ... ok
test_exactly_two_hours_is_allowed (test_booking.BookingTests.test_exactly_two_hours_is_allowed) ... ok
test_existing_unchanged_after_accepted_request (test_booking.BookingTests.test_existing_unchanged_after_accepted_request) ... ok
test_existing_unchanged_after_rejected_request (test_booking.BookingTests.test_existing_unchanged_after_rejected_request) ... ok
test_existing_unchanged_when_blocked (test_booking.BookingTests.test_existing_unchanged_when_blocked) ... ok
test_fits_exactly_between_two_bookings (test_booking.BookingTests.test_fits_exactly_between_two_bookings) ... ok
test_free_slot_among_three_bookings (test_booking.BookingTests.test_free_slot_among_three_bookings) ... ok
test_identical_to_existing_booking_is_rejected (test_booking.BookingTests.test_identical_to_existing_booking_is_rejected) ... ok
test_inside_existing_booking_is_rejected (test_booking.BookingTests.test_inside_existing_booking_is_rejected) ... ok
test_last_minute_of_the_day_is_allowed (test_booking.BookingTests.test_last_minute_of_the_day_is_allowed) ... ok
test_negative_start_is_rejected (test_booking.BookingTests.test_negative_start_is_rejected) ... ok
test_non_integer_time_is_not_handled_but_still_returns_a_boolean (test_booking.BookingTests.test_non_integer_time_is_not_handled_but_still_returns_a_boolean) ... ok
test_now_zero_start_one_is_allowed (test_booking.BookingTests.test_now_zero_start_one_is_allowed) ... ok
test_now_zero_start_zero_is_rejected (test_booking.BookingTests.test_now_zero_start_zero_is_rejected) ... ok
test_one_minute_after_now_is_allowed (test_booking.BookingTests.test_one_minute_after_now_is_allowed) ... ok
test_one_minute_booking_is_allowed (test_booking.BookingTests.test_one_minute_booking_is_allowed) ... ok
test_over_two_hours_is_rejected (test_booking.BookingTests.test_over_two_hours_is_rejected) ... ok
test_overlap_in_unsorted_list_is_rejected (test_booking.BookingTests.test_overlap_in_unsorted_list_is_rejected) ... ok
test_overlap_is_rejected (test_booking.BookingTests.test_overlap_is_rejected) ... ok
test_overlap_over_the_start_is_rejected (test_booking.BookingTests.test_overlap_over_the_start_is_rejected) ... ok
test_overlap_with_second_booking_is_rejected (test_booking.BookingTests.test_overlap_with_second_booking_is_rejected) ... ok
test_result_is_a_boolean_in_every_branch (test_booking.BookingTests.test_result_is_a_boolean_in_every_branch) ... ok
test_reversed_times_are_rejected (test_booking.BookingTests.test_reversed_times_are_rejected) ... ok
test_start_in_the_past_is_rejected (test_booking.BookingTests.test_start_in_the_past_is_rejected) ... ok
test_starting_now_is_rejected (test_booking.BookingTests.test_starting_now_is_rejected) ... ok
test_touching_end_is_allowed (test_booking.BookingTests.test_touching_end_is_allowed) ... ok
test_zero_length_is_rejected (test_booking.BookingTests.test_zero_length_is_rejected) ... ok
 
----------------------------------------------------------------------
Ran 33 tests in 0.000s
 
OK
```
 
### 8.2 The checker, final run
 
Paste the **complete** output of `python tests/check_booking.py`. Paste it **last**: if you edit
this file afterwards, run the checker again and paste again.
 
```text
Week 05 - can_book: the function, your tests, the evidence   (Path A)
 
PASS   F1   the six cases from the task table           6 of 6 cases
PASS   F2   AC1 time order and day bounds               5 of 5 cases
PASS   F3   AC1 the start is in the future              5 of 5 cases
PASS   F4   AC2 at most 120 minutes                     3 of 3 cases
PASS   F5   AC3 a blocked room accepts nothing          2 of 2 cases
PASS   F6   AC4 every kind of overlap is rejected       5 of 5 cases
PASS   F7   AC4 touching endpoints are allowed          3 of 3 cases
PASS   F8   AC4 every existing booking is checked       4 of 4 cases
PASS   F9   AC5 the result is a real Boolean            3 of 3 cases
PASS   F10  AC5 the inputs are left unchanged           2 of 2 cases
PASS   O1   the assistant's first version is kept       v1 kept (27 lines)
PASS   S1   your suite has at least 11 tests            33 tests
PASS   S2   your suite is green on your own code        33 tests, OK
PASS   M1   your tests catch a fault in AC1             caught by test_now_zero_start_zero_is_rejected, test_starting_now_is_rejected
PASS   M2   your tests catch a fault in AC1             caught by test_end_after_midnight_is_rejected
PASS   M3   your tests catch a fault in AC1             caught by test_zero_length_is_rejected
PASS   M4   your tests catch a fault in AC2             caught by test_exactly_two_hours_is_allowed
PASS   M5   your tests catch a fault in AC3             caught by test_blocked_room_is_rejected, test_blocked_room_with_no_bookings_is_rejected, test_existing_unchanged_when_blocked
PASS   M6   your tests catch a fault in AC4             caught by test_ending_at_existing_start_is_allowed, test_fits_exactly_between_two_bookings, test_free_slot_among_three_bookings and 1 more
PASS   M7   your tests catch a fault in AC4             caught by test_existing_unchanged_after_rejected_request, test_overlap_in_unsorted_list_is_rejected, test_overlap_with_second_booking_is_rejected
PASS   M8   your tests catch a fault in AC4             caught by test_containing_existing_booking_is_rejected
PASS   M9   your tests catch a fault in AC5             caught by test_existing_unchanged_after_accepted_request
PASS   M10  your tests catch a fault in AC5             caught by test_existing_unchanged_after_accepted_request, test_existing_unchanged_after_rejected_request
PASS   L1   report 1: tool, model and language          tool, model and language recorded
PASS   L2   report 2: the plan, and what you corrected  plan pasted, 1 row(s) on what you corrected or verified
PASS   L3   report 3: v1 mapped to AC1-AC4              6 conditions mapped, AC1-AC4 all present
PASS   L4   report 4: at least 11 of your tests listed  33 tests listed
PASS   L5   report 5: debugging evidence                1 row(s) of input / expected / actual
PASS   L6   report 6: the critique, each point judged   critique pasted, 5 points judged
PASS   L7   report 7: change log                        1 change-log row(s)
PASS   L8   report 8.1: real output of your suite       suite output pasted
PASS   L9   report 10: conclusion of 120-180 words      148 words
------------------------------------------------------------------------------
v1 (code/original/booking_v1.py): passes F1 F2 F3 F4 F5 F6 F7 F8 F9 F10 - fails nothing - identical to your final: no
SUMMARY pass=32 fail=0 error=0   (32 checks)
Behaviour and shape are clean. This says nothing about the quality of your review.
```
 
### 8.3 Path B only — three faults I planted myself
 
Breaking my own function on purpose is a Path B task. I am on Path A, so this section stays empty; the ten faulty versions in M1–M10 do the same job.
 
| # | Line I changed (before → after) | AC it breaks | Test that failed |
| --- | --- | --- | --- |
| 1 | not applicable (Path A) | not applicable | not applicable |
| 2 | not applicable (Path A) | not applicable | not applicable |
| 3 | not applicable (Path A) | not applicable | not applicable |
 
The three failing runs (Path A students leave this block empty):
 
```text
```
 
---
 
## 9. What still fails, and what the contract does not say
 
### 9.1 Checks I am keeping as FAIL or ERROR
 
The same IDs as `known_fails` in `submission.yml`. Write `none` if the run is clean.
 
| Check | Why it stays |
| --- | --- |
| none | The last checker run has no FAIL and no ERROR: all ten faulty versions M1–M10 were caught by my suite. |
 
### 9.2 Outside the contract
 
The contract says times are integers. It does not say what `can_book` does when one is not —
`600.5`, or the string `"600"`. What does **your** function do, and why is that the right call?
 
- My function does not handle it (`not-handled`). `can_book(600.5, 660.5, 540, False, [])` runs through the same comparisons as an integer and returns a Boolean; a string such as `"600"` would raise `TypeError` at the first comparison with an integer. I added no check because the contract guarantees integers, AC5 only defines True and False for AC1–AC4, and the task says to keep the feature within the stated scope. A type check would be a rule nobody specified, and "raise an exception" would contradict AC5's "Return False otherwise". The test `test_non_integer_time_is_not_handled_but_still_returns_a_boolean` documents the behaviour for floats; it follows no AC, so the checker does not count it for M.
### 9.3 A bound that never decides
 
One of the bounds written in AC1 can never be the *only* reason a request is rejected. Which one,
and why?
 
- `0 <= start`. The contract says `now` is valid, 0–1439, and AC1 also requires `start > now`. Then `start > now >= 0`, so any start below 0 already fails `start > now`. A negative start is always rejected twice, and the lower bound never decides alone. `test_negative_start_is_rejected` therefore passes even without that bound. The other bounds can decide alone: `start < end`, `end <= 1440` and `start > now`.
---
 
## 10. Conclusion (120–180 words)
 
<!-- Answer all three, in your own words, without the assistant:
     (a) Explain the overlap condition in your final code — why those two comparisons, and why
         they let touching bookings through.
     (b) Which fault did your tests miss the longest, and what did the missing test have in common
         with the ones you already had?
     (c) What did you have to decide that neither the contract nor the assistant decided for you?
     Worthless: "the AI made a mistake and I fixed it."
     Worth everything: "F7 failed on can_book(570, 600, ...): v1 compared with <= on the start
     side, so a booking that ends exactly when another begins was rejected." -->
 
<!-- Write your conclusion below this line -->
 
(a) The overlap line is `start < booked_end and booked_start < end`. A request overlaps a booking only if it starts before that booking ends and that booking starts before the request ends. Both comparisons are strict because an interval includes its start and excludes its end: `can_book(660, 720, ...)` against `(600, 660)` gives `660 < 660`, which is false, so touching is allowed. With `<=`, as in the slide's faulty check, that call would be rejected.
 
(b) v1 passed F1–F10 and my suite caught all ten faulty versions, so no fault went unnoticed. M9 was caught by only one test, `test_existing_unchanged_after_accepted_request`; it is the only test that inspects the list after the call instead of the returned value.
 
(c) I decided that a non-integer time is not handled: AC5 says return False and the contract guarantees integers, so I added no validation.
 