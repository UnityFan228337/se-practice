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
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | | | | | | |
| 6 | | | | | | | |
| 7 | | | | | | | |
| 8 | | | | | | | |
| 9 | | | | | | | |
| 10 | | | | | | | |
| 11 | | | | | | | |

---

## 5. Task 4 — debugging with evidence

One row per defect you found — in v1, in a later version, or in your own tests. If v1 passed
everything, the row is the **new edge case you added**, with expected and actual equal, and the
cause column says why no change was needed.

| # | Input (the full call) | Expected | Actual | Cause (quote the line) | Fix | Who proposed the fix |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | | | | | | |

**The debug prompt I sent, and the assistant's answer** (leave the block empty if you did not use it):

```text
```

---

## 6. Task 5 — the critique

**The assistant's critique, pasted unedited:**

```text
(paste here)
```

| # | Suggestion | accept / reject | Reason — cite the AC or the contract line | Suite after the change |
| --- | --- | --- | --- | --- |
| 1 | | accept / reject | | |
| 2 | | accept / reject | | |

---

## 7. Change log — v1 to final

| # | What changed (the line, before → after) | Why | Evidence: the test or check that moved |
| --- | --- | --- | --- |
| 1 | | | |

---

## 8. Evidence — real output

### 8.1 My suite, final run

Paste the **complete** terminal output. For Python: everything `python -m unittest -v` printed.

```text
(paste here)
```

### 8.2 The checker, final run

Paste the **complete** output of `python tests/check_booking.py`. Paste it **last**: if you edit
this file afterwards, run the checker again and paste again.

```text
(paste here)
```

### 8.3 Path B only — three faults I planted myself

Break your own function on purpose, one line at a time, run your suite, restore the line.

| # | Line I changed (before → after) | AC it breaks | Test that failed |
| --- | --- | --- | --- |
| 1 | | | |
| 2 | | | |
| 3 | | | |

The three failing runs (Path A students leave this block empty):

```text
```

---

## 9. What still fails, and what the contract does not say

### 9.1 Checks I am keeping as FAIL or ERROR

The same IDs as `known_fails` in `submission.yml`. Write `none` if the run is clean.

| Check | Why it stays |
| --- | --- |
| | |

### 9.2 Outside the contract

The contract says times are integers. It does not say what `can_book` does when one is not —
`600.5`, or the string `"600"`. What does **your** function do, and why is that the right call?

-

### 9.3 A bound that never decides

One of the bounds written in AC1 can never be the *only* reason a request is rejected. Which one,
and why?

-

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
