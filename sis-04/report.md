# SIS #04 — Report: Evolving the Smart Campus Room Availability Checker

## 1. Setup and starting point

| Item | Value |
| --- | --- |
| Assistant (tool) | Copilot (VS Code) |
| Assistant model | not displayed |
| Starting point | starter |
| Baseline commit | e24073c |
| Language (ts or js) | ts |
| Vitest version | 3.2.7 |
| Where I ran the tests | C:\Users\yar\Desktop\se\se-practice\sis-04\app |

### 1.1 Baseline run

```text
RUN  v3.2.7 C:/Users/yar/Desktop/se/se-practice/sis-04/app

No test files found, exiting with code 1

include: **/*.{test,spec}.?(c|m)[jt]s?(x)
exclude:  **/node_modules/**, **/dist/**, **/cypress/**, **/.{idea,git,cache,output,temp}/**, **/{karma,rollup,webpack,vite,vitest,jest,ava,babel,nyc,cypress,tsup,build,eslint,prettier}.config.*
```

## 2. Context for the assistant

### 2.1 Repository map

```text
app/package.json — project setup, React + Vite + Vitest commands
app/src/main.tsx — app bootstrap and render
app/src/App.tsx — page UI, current time form, room selection and booking logic
app/src/index.css — styling for the room form and results
starter/ — provided reference app that runs before the refactor
README.md — assignment description and fixed requirements
```

### 2.2 The context message as sent

```text
Repository map:
- app/src/App.tsx — page UI, room dropdown, current time and booking form, `ROOMS` array and `check()` logic.
- app/src/index.css — page styling.
- app/src/main.tsx — mounts the app.
- app/package.json — Vite + Vitest commands.
- README.md — fixed requirements and grading constraints.

AC1–AC6:
- AC1: reject start >= end and requests in the past.
- AC2: reject requests longer than 120 minutes.
- AC3: reject a blocked room.
- AC4: reject overlaps; touching endpoints is allowed.
- AC5: return Available/Unavailable without changing booking data.
- AC6: responsive and clear feedback.

F1–F5:
- F1: room capacity must be >= requested attendees.
- F2: room must include all chosen equipment items.
- F3: blocked room cannot be reported available.
- F4: empty state when no rooms match.
- F5: changing the selected room refreshes the availability result.

Constraints:
- no login, payments, live APIs or database
- fictional data only
- keep the room catalog and filtering in separate modules
- do not rewrite the app, only refactor and extend it in small steps

Please assess maintenance risks in the current starter and give a small, safe plan. No code yet.
```

## 3. Codebase analysis (Task 1)

### 3.1 Maintainability risks

| # | Risk | Where (file / function) | Evidence | Priority |
| --- | --- | --- | --- | --- |
| 1 | The room-specific blocked flag is stored in the page, not in the room catalog. | `app/src/App.tsx`, `check()` | The page has a separate `blocked` checkbox and `const room = ROOMS.find(...)`; a selected room can be blocked or not based on UI state, which breaks the idea that each room owns its own status. | High |
| 2 | Availability rules are mixed with the page logic. | `app/src/App.tsx`, `check()` | A single function validates time, duration, blocked status, overlap, and writes the result; this makes AC1–AC5 harder to test and refactor without changing the UI. | High |
| 3 | Room catalog data lives inside the page component. | `app/src/App.tsx` | `ROOMS` is created inside the component file, so the app stores data and form logic together instead of separating the catalog from view logic. | Medium |

### 3.2 Improvement plan — before editing

1. Split the room data into its own `src/rooms.ts` module and keep the catalog separate from the UI.
2. Move the booking rules into `src/booking.ts` and keep `canBook()` responsible for AC1–AC5, while `checkRoom()` uses the selected room.
3. Add `src/filter.ts` with `filterRooms()` for F1–F2 and then test the catalog, booking logic, and the integration between filter and room selection.

### 3.3 One AI suggestion I rejected or modified

| Suggestion (as the assistant made it) | Decision | Why — with the AC, F-rule, test or file behind it |
| --- | --- | --- |
| “Use `equipment.some()` in `filterRooms()` so any selected item matches.” | Rejected | F2 requires all equipment items, not any; using `some()` would incorrectly let a room match `projector + whiteboard` if it only has one of them. This is covered by the requirement and by the F2 test we will add. |

## 4. Feature extension (Task 2)

### 4.1 What I added

<!-- Short: the catalog (how many rooms, which equipment), how the filter is chosen on the page,
     what the empty state says, what happens to an old result when the room changes. -->

(write here)

### 4.2 Demonstration

<!-- One row per screenshot in evidence/. Say what is on it: the filter values, the rooms shown,
     the room selected, the times entered and the result. -->

| Screenshot | What it shows |
| --- | --- |
| `evidence/filter-match.png` | (write here) |
| `evidence/filter-empty.png` | (write here) |
| `evidence/switch-a.png` | (write here) |
| `evidence/switch-b.png` | (write here) |
| `evidence/narrow.png` | (write here) |

## 5. Refactoring (Task 3)

<!-- The diagrams are diagrams/before.puml and diagrams/after.puml (README section 8). -->

### 5.1 Module responsibilities after

| Module or component | Responsibility |
| --- | --- |
| `src/rooms.ts` | (write here) |
| `src/booking.ts` | (write here) |
| `src/filter.ts` | (write here) |
| (write here) | (write here) |

### 5.2 Design decisions

<!-- At least two. The alternative is what you could have done instead (often what the assistant
     proposed). The why names an AC, an F-rule, a test or a risk from 3.1. -->

| Decision | Alternative I did not take | Why |
| --- | --- | --- |
| (write here) | (write here) | (write here) |
| (write here) | (write here) | (write here) |

### 5.3 Duplication removed

<!-- One row per duplicated location that is gone. Count what you can point at, nothing else. -->

| Before (file / function, what was repeated) | After (where it lives now) |
| --- | --- |
| (write here) | (write here) |

## 6. Automated tests (Task 4)

### 6.1 Test plan

<!-- One row per required ID. A test may carry several IDs in its title,
     e.g. test('T06 B1 AC2: exactly 120 minutes is available', …) covers B1 and AC2. -->

| ID | Test title (as in the file) | Input → expected |
| --- | --- | --- |
| AC1 | (write here) | (write here) |
| AC2 | (write here) | (write here) |
| AC3 | (write here) | (write here) |
| AC4 | (write here) | (write here) |
| AC5 | (write here) | (write here) |
| F1 | (write here) | (write here) |
| F2 | (write here) | (write here) |
| F3 | (write here) | (write here) |
| F4 | (write here) | (write here) |
| F5 | (write here) | (write here) |
| B1 | (write here) | (write here) |
| B2 | (write here) | (write here) |
| B3 | (write here) | (write here) |
| B4 | (write here) | (write here) |
| B5 | (write here) | (write here) |
| B6 | (write here) | (write here) |
| INT | (write here) | (write here) |

### 6.2 Commands

<!-- The commands exactly as you typed them, from app/. -->

```text
(paste here)
```

### 6.3 Final run

<!-- The REAL output of the full run on your final code. Every test passes, and the number of
     tests equals what your test files hold (R2). -->

```text
(paste here)
```

## 7. Quality evaluation (Task 5)

<!-- Original = your baseline commit. Final = what you submit. "How I obtained it" says how you
     measured, so someone else could repeat it: "1.1 and 6.3 runs", "counted in 5.3",
     "git ls-files app/src". Do not invent a metric. Tests: write passed/total, e.g. 19/19. -->

| Measure | Original | Final | How I obtained it |
| --- | --- | --- | --- |
| Automated tests passed / total | (write here) | (write here) | (write here) |
| Duplicated logic locations removed | (write here) | (write here) | (write here) |
| Code structure: modules and their responsibilities | (write here) | (write here) | (write here) |
| Remaining limitation | (write here) | (write here) | (write here) |

## 8. AI evidence appendix

<!-- At least three exchanges, one ### 8.N block each: the analysis (Task 1), the plan, and at
     least one implementation, refactoring or test exchange. Copy the block for more.
     The prompt as you sent it; the output may be cut to the part you used, with "[…]" where
     you cut. Verified by: the test, run, file or check that confirmed it — not "it looked right". -->

### 8.1 Exchange 1

**Tool and model:** (write here)
**Date:** (write here)
**Purpose:** (write here)

**Prompt:**

```text
(paste here)
```

**Output used:**

```text
(paste here)
```

**Problems found:** (write here)
**Changes made:** (write here)
**Verified by:** (write here)

### 8.2 Exchange 2

**Tool and model:** (write here)
**Date:** (write here)
**Purpose:** (write here)

**Prompt:**

```text
(paste here)
```

**Output used:**

```text
(paste here)
```

**Problems found:** (write here)
**Changes made:** (write here)
**Verified by:** (write here)

### 8.3 Exchange 3

**Tool and model:** (write here)
**Date:** (write here)
**Purpose:** (write here)

**Prompt:**

```text
(paste here)
```

**Output used:**

```text
(paste here)
```

**Problems found:** (write here)
**Changes made:** (write here)
**Verified by:** (write here)

## 9. Checker results and known fails

<!-- Every check still FAIL or ERROR in your last run of python tests/check_sis.py, and why.
     The same IDs go in submission.yml known_fails. None left? Write: none. -->

| Check | Why it still fails |
| --- | --- |
| (write here) | (write here) |

## 10. AI reflection (Task 6)

<!-- 200–300 words, your own words, no assistant. Answer all five:
     What context did you provide the AI assistant? Which generated suggestions were useful or
     incorrect? What did you personally verify? How did tests influence your engineering
     decisions? What would you improve next? -->

(write here)
