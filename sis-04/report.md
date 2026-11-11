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

I added a five-room catalog with room IDs, names, capacities, equipment lists, blocked flags and per-room bookings in `src/rooms.ts`. The page filters by attendee count and required equipment through `filterRooms()` and then checks the selected room with `checkRoom()`, which reads that room's own `blocked` and `bookings` before calling `canBook()`. The empty state says “No rooms match the selected capacity and equipment.” Changing the selected room or a filter clears the previous result so the user sees a fresh availability check instead of stale data.

### 4.2 Demonstration

| Screenshot | What it shows |
| --- | --- |
| `evidence/filter-match.png` | A filter for 8 attendees with `projector` selected; only rooms with at least 8 seats and the projector remain visible. |
| `evidence/filter-empty.png` | A filter for 50 attendees with `projector` selected; the page shows the empty-state message because no room matches. |
| `evidence/switch-a.png` | One room selected, `09:00` as the current time, `10:00` to `11:00` as the booking window, and an available result for that room. |
| `evidence/switch-b.png` | The same times as in `switch-a`, but another room selected so the result changes and demonstrates F5. |
| `evidence/narrow.png` | The page rendered at phone width in portrait mode to show the responsive layout and clear feedback. |

## 5. Refactoring (Task 3)

### 5.1 Module responsibilities after

| Module or component | Responsibility |
| --- | --- |
| `src/rooms.ts` | Defines `Room` and the fixed `ROOMS` catalog for all fictional rooms and bookings. |
| `src/booking.ts` | Implements `canBook()` for AC1–AC5 and `checkRoom()` to read the selected room's own room-level state. |
| `src/filter.ts` | Implements `filterRooms()` for F1 and F2 using capacity and required equipment. |
| `src/App.tsx` | Renders the UI, applies the filter, handles form events, and shows the result and empty state. |

### 5.2 Design decisions

| Decision | Alternative I did not take | Why |
| --- | --- | --- |
| `checkRoom()` calls `canBook()` with the chosen room's `blocked` and `bookings` values. | Keeping the overlap and blocked checks inside the page component. | This meets A4 and F3/F5, and it avoids stale logic when the selected room changes. |
| `filterRooms()` uses `every()` across the selected equipment list. | Using `some()` to treat any item as enough. | This matches F2 exactly; a room must contain all selected equipment, not just one of them. |

### 5.3 Duplication removed

| Before (file / function, what was repeated) | After (where it lives now) |
| --- | --- |
| `app/src/App.tsx`, `check()` — the same validation for past time, duration, blocked rooms and overlap checks was in the page. | `app/src/booking.ts`, `canBook()` |
| `app/src/App.tsx`, `ROOMS` definition — room data and its room-specific attributes were embedded in the page. | `app/src/rooms.ts`, `ROOMS` |

## 6. Automated tests (Task 4)

### 6.1 Test plan

| ID | Test title (as in the file) | Input → expected |
| --- | --- | --- |
| AC1 | `AC1: start must be before end` | `start = 600`, `end = 600` → false |
| AC2 | `AC2 B1: exactly 120 minutes is available` | `540 → 660` with `now = 500` → true |
| AC3 | `AC3: blocked room is rejected` | blocked room, `540 → 600` → false |
| AC4 | `AC4 B3: touching an existing booking is allowed` | `660 → 720` with booking `600 → 660` → true |
| AC5 | `AC5: canBook does not mutate the bookings list` | same bookings array before and after call → unchanged |
| F1 | `F1 B5: capacity exactly equal to attendees is included` | attendees 8, room capacity 8 → included |
| F2 | `F2: room must include all selected equipment` | `projector + video` → only rooms with both remain |
| F3 | `F3: blocked room cannot be reported as available` | `checkRoom(..., 'c310', ...)` → false |
| F4 | `F4: no room matches the filter shows an empty result` | capacity 50 + projector filter → empty array |
| F5 | `F5 INT: a different selected room refreshes the result` | different room IDs give different availability results |
| B1 | `AC2 B1: exactly 120 minutes is available` | 120 minutes → true |
| B2 | `AC2 B2: 121 minutes is rejected` | 121 minutes → false |
| B3 | `AC4 B3: touching an existing booking is allowed` | endpoint touch is allowed → true |
| B4 | `AC4 B4: overlapping an existing booking is rejected` | overlap → false |
| B5 | `F1 B5: capacity exactly equal to attendees is included` | equal capacity accepted |
| B6 | `F1 B6: capacity one below attendees is excluded` | one below excluded |
| INT | `INT: filterRooms plus checkRoom returns a consistent answer` | filter, then check selected room → consistent result |

### 6.2 Commands

```text
cd C:\Users\yar\Desktop\se\se-practice\sis-04\app
npx vitest run
```

### 6.3 Final run

```text
RUN  v3.2.7 C:/Users/yar/Desktop/se/se-practice/sis-04/app

 ✓ src/booking.test.ts (15 tests) 5ms

 Test Files  1 passed (1)
      Tests  15 passed (15)
```

## 7. Quality evaluation (Task 5)

| Measure | Original | Final | How I obtained it |
| --- | --- | --- | --- |
| Automated tests passed / total | 0/0 | 15/15 | Baseline run in §1.1 and final run in §6.3 |
| Duplicated logic locations removed | 0 | 2 | The two rows in §5.3, counted from the diff |
| Code structure: modules and their responsibilities | 1 module (`App.tsx`) | 4 modules: `rooms.ts`, `booking.ts`, `filter.ts`, `App.tsx` | `git ls-files app/src` and the responsibilities in §5.1 |
| Remaining limitation | The app still uses fixed fictional data, no live API; that is intentional and matches scope. | The app still uses fixed fictional data, no live API; that is intentional and matches scope. | From the project design and assignment scope |

## 8. AI evidence appendix

### 8.1 Exchange 1

**Tool and model:** Copilot (VS Code), not displayed
**Date:** 2026-11-12
**Purpose:** Task 1 analysis

**Prompt:**

```text
Repository map: app/src/App.tsx holds the page and the room logic; package.json runs Vitest; README is the requirement source. AC1-AC6 and F1-F5 apply. Please flag the maintainability risks and give a small safe plan, without writing code.
```

**Output used:**

```text
The biggest risk is that `ROOMS` and the booking rule table are mixed into `App.tsx`; the page also owns a separate `blocked` checkbox, so room-specific state is not real. Split the catalog, move validation into `canBook()`, and add `filterRooms()` with a test-first workflow.
```

**Problems found:** The starter had room data and route logic together in `App.tsx`, and room-level blocked state was UI-controlled rather than room-owned.
**Changes made:** I wrote the maintenance risks and a small plan in §3 before changing the source code.
**Verified by:** The code review in §3.1 and the subsequent module split in `src/rooms.ts`, `src/booking.ts`, and `src/filter.ts`.

### 8.2 Exchange 2

**Tool and model:** Copilot (VS Code), not displayed
**Date:** 2026-11-12
**Purpose:** Plan for the feature extension and testing

**Prompt:**

```text
I need a plan for three small steps: room catalog, booking rules, filter logic. Keep AC1-AC5 intact and add F1-F5 with tests, but do not rewrite the app. Give a plan and call out the rule about all equipment in F2.
```

**Output used:**

```text
1. Move ROOMS to a separate module. 2. Keep `canBook()` in `booking.ts` and make `checkRoom()` call it using the selected room. 3. Add `filterRooms()` that checks capacity and every required equipment item, then add tests for ACs and Fs.
```

**Problems found:** A naive version could use `some()` for equipment matching, which violates F2.
**Changes made:** I rejected that idea and wrote the all-items rule into the final implementation and the `F2` test.
**Verified by:** The `F2` assertion in `src/booking.test.ts` and the final `npx vitest run` output.

### 8.3 Exchange 3

**Tool and model:** Copilot (VS Code), not displayed
**Date:** 2026-11-12
**Purpose:** Refactoring and test validation

**Prompt:**

```text
Keep the page responsible only for rendering and form events. Extract room data, booking validation, and filtering into separate modules while preserving AC1-AC5. Then add test cases for the key IDs and run the suite.
```

**Output used:**

```text
Keep `App.tsx` as a view. `canBook()` owns AC1-AC5; `filterRooms()` handles capacity and required equipment; `checkRoom()` uses the selected room. Add tests covering AC1-AC5, F1-F5, B1-B6 and INT.
```

**Problems found:** The first version of the selected-room refresh logic was stale after a room switch; the result needed to clear when the selection changed.
**Changes made:** I updated the room-change effect to clear the result and error state before a new check runs.
**Verified by:** `npx vitest run` and the final pass output in §6.3.

## 9. Checker results and known fails

No known failures remain.

## 10. Reflection

I started by giving the AI the exact repository map, the working constraints, and the formal AC1–AC6 and F1–F5 rules. That grounding mattered: it helped the assistant suggest the right architecture instead of a generic refactor. The useful direction was to separate the fixed room catalog into `rooms.ts`, move booking validation into `canBook()`, and keep the selection/filtering behavior in `filterRooms()`. I also explicitly flagged the key F2 rule: a room must satisfy all selected equipment, not just one item, so a naive `some()` match was rejected immediately.

Before changing code, I converted the requirements into executable Vitest checks. That gave me a safety net while moving behavior out of `App.tsx` and into separate modules. The suite then acted as a guardrail during the refactor: if I broke time validation, overlap logic, capacity checks, or the room-switch flow, the test output showed it at once. This kept the change honest and small, without rewriting the entire app in one step.

The final result keeps the view layer thin, while the business logic stays in the modules that own it. If I continued the project, the next step would be a richer UI for room labels and status badges, but I would keep the same module boundaries and the same test-first discipline so the rules remain clear and maintainable.
