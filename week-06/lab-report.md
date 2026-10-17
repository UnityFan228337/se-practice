# Week 06 — Lab report

**Name:** Maltsev Yaroslav  
**Group:** [CSCI-2208] Software Engineering - Fall 2026
**Date:** 6.10

Fill in every section. **Do not delete, rename or renumber the headings** — the checker and the
grader find your answers by them. Add rows to any table; never remove its header.

---

## 1. Setup

| | |
| --- | --- |
| Tool | Bolt.new |
| Exact model (as Bolt shows it, or `not displayed`) | `not displayed` |
| Bolt project link (or `not shared`, and why) | https://bolt.new/p/72096950 <!-- https://smart-campus-room-av-p15h.bolt.host --> |
| Browser and version | Cent Browser 5.2.1168.83 |
| If you could not use Bolt.new: the tool you used instead, and why | |

---

## 2. Task 1 — define before generating

**Two predictions, written BEFORE you send the first prompt.** Where do you expect v1 to go wrong?
Fill the first three columns now; fill the last one after Task 3.

| # | What I expect to go wrong | AC it concerns | Was I right? (after Task 3) |
| --- | --- | --- | --- |
| 1 | reversed time | AC1 |  |
| 2 | size of buttons for mobile or desktop interface | AC-6 | |

**The initial prompt exactly as I sent it** — the deck's prompt with AC1–AC6 pasted in place of
`[paste AC1–AC6]`, nothing else changed:

```text
Build a small responsive Smart Campus Room Availability Checker. Requirements:
AC1: Accept a candidate interval only when 0 ≤ start < end ≤ 1440 and start is after the supplied current time. AC2: Reject a booking longer than 120 minutes. AC3: Reject the request when the selected room is blocked. AC4: Reject any interval that overlaps an existing booking; touching endpoints are allowed. AC5: Show a clear Available / Unavailable decision without changing the existing booking data. AC6: The page remains usable at desktop and narrow/mobile width and gives understandable validation feedback.

Use fictional sample data only. Keep the implementation simple and within one-page scope. Do not add authentication, backend services, analytics, or unrelated features. After building, briefly list the main files/components you created.
```

---

## 3. Task 2 — prototype v1

v1 export saved in `original/` and screenshot saved as `evidence/v1.png` **before** any cleanup
prompt: yes

**Bolt's list of the files/components it created, pasted unedited:** yes

```text
src/App.tsx
src/index.css
src/main.tsx
src/vite-env.d.ts
src/components/ResultBanner.tsx
src/components/RoomCard.tsx
src/components/TimeField.tsx
src/components/Timeline.tsx
src/data/rooms.ts
src/lib/availability.ts
eslint.config.js
index.html
package.json
package-lock.json
postcss.config.js
tailwind.config.js
tsconfig.json
tsconfig.app.json
tsconfig.node.json
vite.config.ts

```

**What v1 does — one line per thing that works, or visibly does not:**

-

**Repair prompt** (only if the first build did not run — the deck allows one, then the result is
v1). Leave empty if you did not need it:

```text
```

---

## 4. Task 3 — the nine cases

Base for every case unless the row says otherwise: **current time 09:00**, room **not blocked**,
the room's **only booking 10:00–11:00**. The Expected column comes from AC1–AC6 — do not change it.
Write each result exactly as **Available**, **Unavailable** or **Not testable** (the page gives you
no way to set up the case). Save each final run as `evidence/final-T<n>.png`.

| # | Case | What you set up and request | Expected | AC | Result on v1 | Result on final | Final screenshot |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | Touching | 11:00–12:00 | Available | AC4 | Available | Available / Unavailable / Not testable | final-T1.png |
| T2 | Overlap | 10:30–11:30 | Unavailable | AC4 |  Unavailable  | Available / Unavailable / Not testable | final-T2.png |
| T3 | Blocked | 11:00–12:00, room blocked | Unavailable | AC3 |  Unavailable  | Available / Unavailable / Not testable | final-T3.png |
| T4 | Exactly 2 hours | 12:00–14:00 | Available | AC2 | Available | Available / Unavailable / Not testable | final-T4.png |
| T5 | Over 2 hours | 12:00–14:01 | Unavailable | AC2 |  Unavailable | Available / Unavailable / Not testable | final-T5.png |
| T6 | Starts now | 09:00–09:30 (current time 09:00) | Unavailable | AC1 | Available | Available / Unavailable / Not testable | final-T6.png |
| T7 | Reversed times | 12:00–11:00, and the page says why | Unavailable | AC1, AC6 |  Unavailable  | Available / Unavailable / Not testable | final-T7.png |
| T8 | Same check twice | T1, then T1 again without reloading | Available | AC5 | Available  | Available / Unavailable / Not testable | final-T8.png |
| T9 | Narrow screen | T1 at about 375 px wide | Available | AC6 | Available  | Available / Unavailable / Not testable | final-T9.png |

---

## 5. Issue log — cleanup targets

One row per issue you chose to act on (or deliberately not act on). At least **two**: one
functional and one usability or code-quality issue when you have them. If v1 passed every case,
log a justified cleanup that preserves behaviour. Save a screenshot of each as
`evidence/issue-<n>.png`.

| # | Issue | Evidence: steps → expected → observed | Priority | Decision |
| --- | --- | --- | --- | --- |
| 1 | Functional — Start time equal to current time incorrectly accepted (AC1) | Steps: Set the current time to 09:00. Enter a candidate booking interval of 09:00–09:30. Click "Check Availability". → Expected: The request is rejected with a validation error because AC1 dictates that the start time must be after the supplied current time (start > current). → Observed: The prototype accepts the interval as "Available" due to a naive start >= current comparison check in the validation script. | High  | Fix |
| 2 | Functional / State — Submitting identical check request twice modifies or fails to clear transient validation state (AC5) | Steps: Input a valid candidate slot (e.g., 11:00–12:00) and check availability (passes as Available). Without reloading the page or changing fields, click "Check Availability" a second time (matching test case T8). → Expected: The component should successfully re-evaluate and display the "Available" decision consistently without retaining stale validation caches or throwing state exceptions (per AC5). → Observed: The result banner or internal component state occasionally fails to re-render cleanly or retains outdated error styles from previous checks if event listeners aren't fully reset on re-submission. |  Medium  | Defer |

---

## 6. Task 4 — cleanup with focused prompts

One issue per prompt. Paste every prompt **as sent** (every `[bracketed field]` and `AC#` filled
in) and Bolt's answer, unedited.

**Functional fix prompt, as sent, and Bolt's answer:**

```text
In the current prototype, Set the current time to 09:00. Enter a candidate booking interval of 09:00–09:30. Click "Check Availability". produces The prototype accepts the interval as "Available" due to a naive start >= current comparison check in the validation script, but AC1 requires The request is rejected with a validation error because AC1 dictates that the start time must be after the supplied current time (start > current). Make the smallest change that fixes this behavior. Preserve the other acceptance criteria. Explain which file/component you changed and why.


0123456789
 actions taken
Now let me also fix the UI-side validation in App.tsx, which has the same startMin < currentMinutes check used for the error message under the Start time field.


0123456789
 actions taken
Build passes. Here's what I changed and why:

Files changed:

src/lib/availability.ts — The core availability logic. Changed start < currentMinutes to start <= currentMinutes in the AC1 check. This means a start time equal to the current campus time is now rejected, which is what AC1 requires (start must be after current time, not equal to it).

src/App.tsx — The inline validation error shown under the Start time field. Made the same < → <= change so the UI error message matches the actual rejection logic.

Result: With campus time set to 09:00 and a candidate interval of 09:00–09:30, the app now rejects the booking with "Start time must be after the current time (09:00)." instead of accepting it. All other acceptance criteria (end-before-start, max duration, blocked rooms, overlap detection) are untouched.

```

**Cleanup prompt, as sent, and Bolt's answer:**

```text
Review only the validation/computation logic split between App.tsx and availability.ts. for unnecessary duplication, confusing naming, or UI feedback problems. Suggest one small cleanup. Do not add features or redesign the whole application. Implement it only if it preserves AC1–AC6.

I'll review the validation logic split between availability.ts and App.tsx — the area we just touched.


0123456789
 files read
Here's my review of [the validation logic split between App.tsx and availability.ts].

Finding: handleCheck calls checkAvailability(...) even though livePreview already computes the exact same result on every render. This is a redundant recomputation — the data hasn't changed between the last render and the click.

Cleanup: Make handleCheck reuse the already-computed livePreview value instead of calling checkAvailability a second time. This eliminates the duplication without changing any behavior or acceptance criteria.


0123456789
 actions taken
Build passes. Here's the review summary:

Area reviewed: The validation/computation logic split between App.tsx and availability.ts.

Issue found: handleCheck was calling checkAvailability() a second time to produce a result that livePreview had already computed on the same render. Same inputs, same function, same output — pure duplication.

Fix applied: handleCheck now reuses the already-computed livePreview value. This doesn't change any acceptance criteria (AC1–AC6) — the result is identical, we just compute it once instead of twice.

No other issues found: The startError/endError inline checks in App.tsx serve a different purpose (real-time field-level error messages) than checkAvailability (the full validation including room state), so they aren't redundant — they catch problems before a room is even selected.






```

Add further blocks for further prompts.

**Every change or suggestion Bolt made, judged.** Accepting is a decision; so is rejecting. Cite
the AC (or the scope) that justifies it.

| # | What Bolt changed or suggested | accept / reject | Reason — cite the AC or the scope | Retest: which cases, result |
| --- | --- | --- | --- | --- |
| 1 | | accept / reject | | |
| 2 | | accept / reject | | |

---

## 7. Change log — v1 to final

Two to four concrete changes, each one retested.

| # | Issue | Decision | Change (file or component) | Result after retest |
| --- | --- | --- | --- | --- |
| 1 | | | | |
| 2 | | | | |

---

## 8. One generated component, in my own words

Pick one file or component Bolt generated that matters for AC1–AC5 — the one that decides
availability is the best choice. Name its path in backticks, then explain in your own words, without
the assistant, what it does and how it decides. 60 words or more.

**File:** `(write here, e.g. src/App.tsx)`

<!-- Write your explanation below this line -->

---

## 9. What still fails, and what the criteria do not say

### 9.1 Checks I am keeping as FAIL or ERROR

The same IDs as `known_fails` in `submission.yml`. Write `none` if the run is clean.

| Check | Why it stays |
| --- | --- |
| | |

### 9.2 The end of the day

AC1 allows `end ≤ 1440` — a booking may end at 24:00. Can a user of your final page ask for
23:00–24:00? How — and if not, why is that acceptable or not? (This is the value you declare in
`submission.yml` under `assumptions.end_of_day`.)

-

### 9.3 Which "now"?

AC1 says "after the supplied current time". What did **v1** use as the current time, and what did
that mean for testing case T6?

-

---

## 10. Conclusion (120–180 words)

<!-- Answer all three, in your own words, without the assistant:
     (a) Which of your two predictions in section 2 was right, and what did v1 actually get wrong?
     (b) Which AI suggestion did you reject, or would have been wrong to accept, and why?
     (c) What is the difference between "the prototype looks finished" and "the prototype meets
         AC1-AC6" - shown with one case from section 4?
     Worthless: "Bolt made some mistakes and I fixed them."
     Worth everything: "T8 failed on v1: the Check button also added the booking to the list, so
     checking 11:00-12:00 a second time said Unavailable. AC5 says the check must not change the
     booking data." -->

<!-- Write your conclusion below this line -->
