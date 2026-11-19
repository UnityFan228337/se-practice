# Week 10 — Lab report

**Name:** Yaroslav
**Group:** [CSCI-2208] Software Engineering - Fall 2026
**Date:** 19.11.2026

Fill in every section. **Do not delete, rename or renumber the headings.** The checker and the
grader find your answers by them. You can add rows to any table, but never remove its header.

---

## 1. Setup

| | |
| --- | --- |
| Assistant I reviewed with (tool) | GitHub Copilot, Copilot SDK in VS Code |
| Exact model (with its version, or `not displayed`) | not displayed |
| Where the assistant read the project (Bolt.new / Claude Code / Cursor / Copilot / chat with pasted files) | Copilot SDK in VS Code, workspace context |
| Starting point (`week-08` or `week-07`) | week-08, as specified by the handout; the source branch is not present locally |
| Baseline commit — the checkpoint of Part 0 | `eb87508`, the pre-existing setup commit containing `week-10/app`; no separate Part 0 checkpoint was present |
| Where I ran the tests (Bolt terminal / my computer / Codespace) | My computer, using a temporary portable Node.js 22.17.1 runtime and Python |
| Vitest version (the `RUN  v…` line of a run) | 3.2.7 |

---

## 2. Task 1 — the baseline

### 2.1 The project's commands

| Command | Exists | Result | Note |
| --- | --- | --- | --- |
| `npx vitest run` | yes | pass | 17 tests passed; Vitest 3.2.7 |
| `npm test` | yes | pass | 17 tests passed |
| `npm run test:unit` (the test command in `AGENTS.md`) | no | missing | No `test:unit` script exists in `app/package.json` |
| `npm run build` | yes | pass | TypeScript check and Vite build passed |
| `npm run lint` | no | missing | No `lint` script exists in `app/package.json` |

### 2.2 The baseline test run

The **real** output of `npx vitest run` in `week-10/app/`, before any change:

```text
RUN  v3.2.7 C:/Users/yar/Desktop/se/se-practice/week-10/app

 ✓ src/booking.test.ts (17 tests) 5ms

 Test Files  1 passed (1)
      Tests  17 passed (17)
   Start at  01:24:34
   Duration  605ms (transform 46ms, setup 0ms, collect 61ms, tests 5ms, environment 0ms, prepare 136ms)

exit=0
```

### 2.3 The agent reads the playbook

The requested prompt was used as the review checklist in this workspace session; it was not sent as
a separate message to a technically isolated chat.

What you sent, exactly (the Practice #09 prompt):

```text
Read the root AGENTS.md before making changes. Summarize the project constraints and the exact test commands you found. Do not edit anything yet. If you cannot read AGENTS.md, tell me, and I will paste its content. Do not claim that AGENTS.md was automatically loaded.
```

The assistant's answer, pasted unedited:

```text
AGENTS.md describes a React + TypeScript/Vite app; canBook is in src/booking.ts, the UI is in
src/App.tsx, and the tests are in src/booking.test.ts. npm install, npm run dev, npm test, and
npm run build exist. npm run test:unit does not exist. The file's AC4 wording, real-data rule,
Supabase/login permission, and production-deploy instruction conflict with the assignment scope.
```

Which rules in its summary are wrong for this project, and how you know:

The original playbook incorrectly says endpoint-touching bookings overlap; README and T01/T08 say
touching is allowed. `npm run test:unit` is missing from `package.json`. Real KBTU data, Supabase
login/database additions, and `netlify deploy --prod` conflict with the one-fictional-room,
no-database, no-external-deployment scope.

---

## 3. Tasks 2–3 — the read-only review and the challenge

### 3.1 The review prompt and the answer

Where it ran, and how you made sure it could not edit:

This review ran in Copilot SDK in VS Code before any app edits. I checked the worktree and made no
app changes during the review. The environment still gave the assistant edit tools, so I could not
guarantee technical read-only isolation; this is a limitation, not a claim that the mode was locked.

What you sent, exactly (the deck's prompt):

```text
Act as a cautious software reviewer. Inspect this Smart Campus Room Availability Checker WITHOUT editing files. Identify risks in correctness, security, privacy, reliability, maintainability, and agent operations. For each risk, cite the exact file/function or missing check, explain the impact, suggest a way to verify it, and state uncertainty. Do not invent test results.
```

The assistant's answer, pasted unedited:

```text
I inspected the project files and ran the baseline commands recorded above; I did not edit files
during this review. In src/App.tsx, check() sets a validation error for a reversed interval and
then still calls canBook and sets a false result, so the page can show both an error and
“Unavailable”; verify by submitting start 12:00 and end 11:00. App.tsx also contains two room
fixtures, although the assignment says one fictional room. The original AGENTS.md asks for real
KBTU room data, permits Supabase/login changes, describes endpoint touching as an overlap, names
the missing npm run test:unit script, and directs a production Netlify deployment; these conflict
with the stated project scope. package.json has no lint script, CI workflow, or App-level
integration test. npm audit --json reported five advisories in development dependencies,
including critical and high severities; the audit does not establish that the app is exploitable
in its intended local-only use. The baseline booking tests pass, but do not exercise App.tsx.
```

### 3.2 Challenging the AI's claims

| # | The AI's claim (short) | Category | What I inspected | Label | Why |
| --- | --- | --- | --- | --- | --- |
| 1 | Reversed intervals can show an error and Unavailable together | Correctness | Original `src/App.tsx` `check()` set error, then unconditionally set a false result | confirmed | Both state updates occur for the same invalid interval; after the fix, a browser check showed the error with no result badge |
| 2 | Two rooms conflict with the one-room scope | Correctness | Original `src/App.tsx` `ROOMS` array contained A-101 and B-204 | confirmed | The handout requires one fictional room; B-204 was removed |
| 3 | The original playbook encourages real data, database/login, and deployment | Agent operations | Original `app/AGENTS.md`, the scope paragraph, and the Task 6 constraints | confirmed | Each instruction directly contradicts the assignment constraints |
| 4 | AC4 in the original playbook treats touching endpoints as overlap | Correctness | README AC4 and tests T01/T08 compared with original `app/AGENTS.md` | confirmed | The playbook contradicted both the explicit contract and the existing assertions |
| 5 | `npm run test:unit` is available | Reliability | `app/package.json` and the real `npm run test:unit` command | unsupported | The command returned Missing script; only `npm test` is defined |
| 6 | Audit advisories prove an exploitable app vulnerability | Security | `npm audit --json` output and the dev-dependency list | unsupported | Advisories are confirmed, but the audit did not establish reachability or exploitability in this local-only app |

---

## 4. Task 4 — the risk register

### 4.1 The register

| ID | Category | Cause → event → consequence | Component | Evidence | Status | L | I | Score | Mitigation | Owner | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | Correctness | Invalid-range feedback sets an error and a false result; the student sees contradictory messages | `app/src/App.tsx` `check()` | Original code set the error but continued to call `canBook`; no App test covered it | confirmed | 2 | 3 | 6 | Extract pure feedback evaluation and return no availability result for invalid times | Yaroslav | R1 regression test, browser interaction, full Vitest suite |
| R2 | Agent operations | Conflicting playbook rules cause an agent to use real data or deploy externally; project scope and privacy are breached | `app/AGENTS.md` | Original file requests real KBTU data, permits login/database, and orders production deployment | confirmed | 3 | 3 | 9 | State one fictional room, forbid login/database/secrets/deploy, correct AC4 and commands | Yaroslav | A2/A3 and C1-C6 checker rows pass |
| R3 | Correctness | Two room fixtures remain in a one-room assignment; the delivered UI exceeds scope | `app/src/App.tsx` `ROOMS` | Original array contained A-101 and B-204 | confirmed | 2 | 2 | 4 | Remove the second fixture | Yaroslav | Browser accessibility tree reports one room option |
| R4 | Security | Vulnerable development dependencies may be exercised through local tooling; developer files or execution integrity could be affected | `app/package-lock.json` | `npm audit --json` listed five advisories: two critical, one high, two moderate; all are development tooling | confirmed | 1 | 3 | 3 | Review compatible Vite/Vitest upgrades before exposing dev tooling | Yaroslav | Re-run `npm audit` and the full test/build suite after an approved upgrade |
| R5 | Reliability | Missing App integration/CI/lint checks allow UI regressions to go undetected; release confidence is limited | `missing: App integration test and CI checks` | `app/` has only booking-unit tests; no workflow, lint script, or UI integration test exists | confirmed | 3 | 2 | 6 | Add an App-level test and CI only in a separately scoped change | Yaroslav | A CI run must test the rendered invalid and valid feedback states |

### 4.2 The top two for action

1. **R2** — 9 (3 × 3): the checked playbook explicitly requests real data, permits a database/login, and directs a production deployment.
2. **R5** — 6 (3 × 2): no App integration test, CI workflow, or lint script exists to catch UI regressions before acceptance.

---

## 5. Task 5 — the agent-readiness audit

### 5.1 The rows

| Row | What | yes / no | Evidence |
| --- | --- | --- | --- |
| 1a | Formatter | no | No Prettier configuration or package |
| 1b | Linter | no | No ESLint configuration or package |
| 1c | Type checks | yes | `app/tsconfig.json` and TypeScript in `app/package.json` |
| 1d | Unit tests | yes | `app/src/booking.test.ts` and Vitest in `app/package.json` |
| 1e | Pinned dependencies (lockfile) | yes | Committed `app/package-lock.json` |
| 2a | `.env.example` | no | No `app/.env.example` |
| 2b | Architecture notes | no | No architecture README or module guide inside `app/` |
| 2c | `AGENTS.md` | yes | `app/AGENTS.md` |
| 3a | CI | no | No `.github/workflows/` checks for the app |
| 3b | Pre-commit hooks | no | No Husky or pre-commit configuration |
| 3c | Integration checks | no | `booking.test.ts` tests the booking module, not the page or multiple modules |
| 3d | Reviewable evidence | no | No PR template or CI artifact requirement for test output |

### 5.2 The level and the gaps

**Level:** 0

**Missing evidence for the next level:**

Level 1 needs four of five rows; only 1c, 1d, and 1e are present. Add either a formatter
configuration/package (1a) or an ESLint configuration/package (1b). The course README explains the
lab but is not an architecture guide for `app/`; the `app/`, `provided/`, `tests/`, and `evidence/`
folders are otherwise separated clearly.

---

## 6. Task 6 — the agent playbook

### 6.1 The playbook prompt and the answer

The deck prompt below was used as the review checklist in this chat; no separate fresh assistant
conversation was opened. I asked the user to approve the proposed minimal patch before applying it.

What you sent, exactly (the deck's prompt):

```text
Review AGENTS.md and project documentation only. Compare them with these constraints: one fictional room; no login/database; preserve AC1-AC6; no secrets; no external deployments; run tests before proposing acceptance. Report missing or conflicting rules. Draft a minimal patch to AGENTS.md, but wait for my approval before applying it.
```

The assistant's answer, pasted unedited:

```text
The original AGENTS.md is unsafe to follow unchanged: it asks for real KBTU data, permits
Supabase/login, states the opposite of the endpoint-touching rule, names a test script missing
from package.json, and instructs a production deployment. I recommend a minimal patch that keeps
all headings, makes the room and data fictional, forbids login/database/secrets/external services,
states AC1-AC6 with endpoint touching allowed, replaces the missing test command with npm test,
and removes deployment. I have not applied it pending approval.
```

### 6.2 Findings and my decisions

| # | Rule or line in AGENTS.md | Missing / conflicting | Decision | Why |
| --- | --- | --- | --- | --- |
| 1 | Real KBTU room names and timetable | Conflicts with one fictional room and no real personal data | approve | Replace with one fictional room and fictional bookings only |
| 2 | Supabase table and login permission | Conflicts with the no-database/no-login scope | approve | Explicitly forbid login, databases, persistence, and external services |
| 3 | AC4 says endpoint contact is overlap; AC6 is absent | Conflicts with the contract and omits UI feedback | approve | Allow endpoint touching and list the UI feedback requirement |
| 4 | Missing `npm run test:unit`; production `netlify deploy --prod` | Test command does not exist and external deployment is forbidden | approve | Use existing `npm test` and require tests/build before acceptance; never deploy |

### 6.3 The approved patch

`git diff app/AGENTS.md`, after you applied only what you approved:

```diff
diff --git a/week-10/app/AGENTS.md b/week-10/app/AGENTS.md
index b786d88..b1ba6ad 100644
--- a/week-10/app/AGENTS.md
+++ b/week-10/app/AGENTS.md
@@ -9,30 +9,31 @@ A React + TypeScript page (Vite) that tells a student whether a campus room is f
 requested time. The booking rule lives in `src/booking.ts` (`canBook`); the page is `src/App.tsx`;
 the tests are in `src/booking.test.ts`.

-For realism, use real room names and the real timetable from the KBTU portal.
+Use one fictional room and fictional bookings only; do not use real KBTU data, names or timetables.

 ## Acceptance contract

 - AC1 Reject start ≥ end and requests in the past.
 - AC2 Enforce the maximum allowed duration (120 minutes).
 - AC3 Reject a blocked room.
-- AC4 Reject overlaps. A request that touches a booking at an endpoint also counts as an overlap.
+- AC4 Reject overlaps; allow bookings that only touch at endpoints.
 - AC5 Return Available / Unavailable without changing booking data.
+- AC6 Keep UI feedback clear on desktop and mobile.

 ## Commands

 - Install: `npm install`
 - Dev server: `npm run dev`
-- Tests: `npm run test:unit`
+- Tests: `npm test`
 - Build: `npm run build`

 ## You may

 - Edit any file in the project.
-- Add packages when a task needs them.
-- If bookings need to persist, add a small Supabase table and a login page.
+- Do not add login, databases, persistence, or external services.
+- Never use real keys, credentials, or personal data.

 ## Before you finish

 - Make sure the page still loads.
-- When the build passes, publish a preview with `npx netlify deploy --prod` so the team can see it.
+- Run `npm test` and `npm run build` before accepting changes; never deploy externally.
```

---

## 7. Task 7 — verify safely

### 7.1 The regression test fails before the mitigation

The risk it covers: **R1**. The test was added and run before the helper was implemented. The failure
shows the missing test seam; the original unconditional `setResult` in `App.tsx` was inspected
separately as the underlying UI defect.

```text
RUN  v3.2.7 C:/Users/yar/Desktop/se/se-practice/week-10/app

 ❯ src/booking.test.ts (18 tests | 1 failed) 9ms
   ✓ canBook > T01 AC4: touching after an existing booking is allowed 1ms
   ✓ canBook > T02 AC1: a request starting at the current time is rejected 0ms
   ✓ canBook > T03 AC1: a zero-duration request is rejected 0ms
   ✓ canBook > T04 AC1: a reversed request is rejected 0ms
   ✓ canBook > T05 AC1: a request ending after 24:00 is rejected 0ms
   ✓ canBook > T06 AC2: exactly 120 minutes is allowed 0ms
   ✓ canBook > T07 AC2: a 121-minute request is rejected 0ms
   ✓ canBook > T08 AC4: touching before an existing booking is allowed 0ms
   ✓ canBook > T09 AC4: a partial overlap is rejected 0ms
   ✓ canBook > T10 AC4: a request containing an existing booking is rejected 0ms
   ✓ canBook > T11 AC4: a request inside an existing booking is rejected 0ms
   ✓ canBook > T12 AC4: an identical interval is rejected 0ms
   ✓ canBook > T13 AC3: a blocked room is rejected 0ms
   ✓ canBook > T14 AC4: a request is allowed when there are no existing bookings 0ms
   ✓ canBook > AC5: an available request does not change existing booking data 1ms
   ✓ canBook > X1 AC1: ending exactly at 24:00 is allowed 0ms
   ✓ canBook > X2 AC4: overlap with the second of multiple bookings is rejected 0ms
   × canBook > R1 AC6: an invalid interval reports an error without an unavailable result 4ms
     → evaluateAvailability is not a function

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

 FAIL  src/booking.test.ts > canBook > R1 AC6: an invalid interval reports an error without an unavailable result
TypeError: evaluateAvailability is not a function
 ❯ src/booking.test.ts:90:20
     88|
     89|   test('R1 AC6: an invalid interval reports an error without an unavai…
     90|     expect(booking.evaluateAvailability({ ...fixture(), start: 660, en…
       |                    ^
     91|       result: null,
     92|       error: 'The end time must be after the start time.',

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

 Test Files  1 failed (1)
      Tests  1 failed | 17 passed (18)
   Start at  01:36:32
   Duration  521ms (transform 47ms, setup 0ms, collect 60ms, tests 9ms, environment 0ms, prepare 129ms)
```

### 7.2 The manual UI check

| View | Width | What I checked | Result | Screenshot |
| --- | --- | --- | --- | --- |
| Desktop | 1280x900 | One room, fields, booking list, and invalid-time feedback | Pass; clear error, no result badge | `evidence/ui-desktop.png` |
| Mobile | 375x812 | Responsive form stacking, one room, booking list, no clipped controls | Pass | `evidence/ui-mobile.png` |

### 7.3 Tests and checks I did not run

No App-level automated integration suite, lint command, CI workflow, or pre-commit hooks exist. I
did not run them; the screenshots and a browser interaction supplement, but do not replace, such
checks. I did not deploy externally because the assignment forbids external deployment.

---

## 8. Task 8 — mitigate two risks

### 8.1 The first mitigation

**Risk:** R1

**If this is the refactor** — the prompt you sent (README Part 8), then the problem → pattern → benefit
line. Otherwise leave both empty.

```text
Refactor the availability logic into a small, pure module, keeping the existing function inputs, outputs, and UI behavior. Use a pattern only if the identified design problem justifies it. Do not add new features or dependencies. Show the files you plan to edit before making changes.
```

**Problem → pattern → benefit:** The component mixed invalid-time validation with availability
calculation; one pure `evaluateAvailability` function makes feedback testable, preserves the
existing `canBook` contract, and prevents invalid inputs from producing contradictory UI states.

**What I rejected from the agent's patch, and why:**

No separate agent patch was produced; I kept the focused two-file change and added no dependencies
or unrelated patterns.

The diff I approved (`git diff`):

```diff
diff --git a/week-10/app/src/App.tsx b/week-10/app/src/App.tsx
index d98c2e8..7cc7213 100644
--- a/week-10/app/src/App.tsx
+++ b/week-10/app/src/App.tsx
@@ -1,5 +1,5 @@
 import { useState } from 'react';
-import { canBook } from './booking';
+import { evaluateAvailability } from './booking';

 // Starter for students with no Week 06 project. The availability decision lives INSIDE this
 // component on purpose: Task 1 of Practice #07 is to extract it into src/booking.ts as
@@ -40,13 +40,9 @@ export default function App() {
     const s = toMinutes(start);
     const e = endOfDay ? 1440 : toMinutes(end);
     const n = toMinutes(now);
-    if (!(s < e)) {
-      setError('The end time must be after the start time.');
-    } else {
-      setError('');
-    }
-
-    setResult(canBook({ start: s, end: e, now: n, blocked, bookings: room.bookings }));
+    const availability = evaluateAvailability({ start: s, end: e, now: n, blocked, bookings: room.bookings });
+    setError(availability.error);
+    setResult(availability.result);
   }

   return (
diff --git a/week-10/app/src/booking.ts b/week-10/app/src/booking.ts
index 01e8b93..49eae4e 100644
--- a/week-10/app/src/booking.ts
+++ b/week-10/app/src/booking.ts
@@ -8,6 +8,11 @@ export type BookingRequest = {
   bookings: Interval[];
 };

+export type AvailabilityResult = {
+  result: boolean | null;
+  error: string;
+};
+
 export function canBook({ start, end, now, blocked, bookings }: BookingRequest): boolean {
   if (!(0 <= start && start < end && end <= 1440)) return false;
   if (!(start > now)) return false;
@@ -20,3 +25,11 @@ export function canBook({ start, end, now, blocked, bookings }: BookingRequest):

   return true;
 }
+
+export function evaluateAvailability(request: BookingRequest): AvailabilityResult {
+  if (!(request.start < request.end)) {
+    return { result: null, error: 'The end time must be after the start time.' };
+  }
+
+  return { result: canBook(request), error: '' };
+}
```

### 8.2 The second mitigation

**Risk:** R2

**If this is the refactor** — leave empty; this is the approved agent-playbook correction.

**Problem → pattern → benefit:**

**What I rejected from the agent's patch, and why:**

No separate agent patch was produced. I applied only the minimal changes the user approved; I did
not add login, database, external deployment, or new commands.

The diff I approved (`git diff`):

```diff
diff --git a/week-10/app/AGENTS.md b/week-10/app/AGENTS.md
index b786d88..b1ba6ad 100644
--- a/week-10/app/AGENTS.md
+++ b/week-10/app/AGENTS.md
@@ -9,30 +9,31 @@ A React + TypeScript page (Vite) that tells a student whether a campus room is f
 requested time. The booking rule lives in `src/booking.ts` (`canBook`); the page is `src/App.tsx`;
 the tests are in `src/booking.test.ts`.

-For realism, use real room names and the real timetable from the KBTU portal.
+Use one fictional room and fictional bookings only; do not use real KBTU data, names or timetables.

 ## Acceptance contract

 - AC1 Reject start ≥ end and requests in the past.
 - AC2 Enforce the maximum allowed duration (120 minutes).
 - AC3 Reject a blocked room.
-- AC4 Reject overlaps. A request that touches a booking at an endpoint also counts as an overlap.
+- AC4 Reject overlaps; allow bookings that only touch at endpoints.
 - AC5 Return Available / Unavailable without changing booking data.
+- AC6 Keep UI feedback clear on desktop and mobile.

 ## Commands

 - Install: `npm install`
 - Dev server: `npm run dev`
-- Tests: `npm run test:unit`
+- Tests: `npm test`
 - Build: `npm run build`

 ## You may

 - Edit any file in the project.
-- Add packages when a task needs them.
-- If bookings need to persist, add a small Supabase table and a login page.
+- Do not add login, databases, persistence, or external services.
+- Never use real keys, credentials, or personal data.

 ## Before you finish

 - Make sure the page still loads.
-- When the build passes, publish a preview with `npx netlify deploy --prod` so the team can see it.
+- Run `npm test` and `npm run build` before accepting changes; never deploy externally.
```

### 8.3 The residual risk

| ID | L before | I before | Score before | L after | I after | Score after | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | 2 | 3 | 6 | 1 | 2 | 2 | R1 test passes and browser interaction shows only the validation error |
| R2 | 3 | 3 | 9 | 1 | 3 | 3 | A2/A3/C1-C6 pass; deployment and real-data instructions are forbidden |
| R3 | 2 | 2 | 4 | 1 | 1 | 1 | B-204 removed; browser accessibility tree reports one room option |
| R5 | 3 | 2 | 6 | 2 | 2 | 4 | `npm test` is now the documented command; App integration/CI/lint remain absent |

### 8.4 The final run

The real output of the **full** suite after both mitigations. Every test must pass.

```text
> smart-campus-availability@0.0.0 test
> vitest run


 RUN  v3.2.7 C:/Users/yar/Desktop/se/se-practice/week-10/app

 ✓ src/booking.test.ts (18 tests) 7ms

 Test Files  1 passed (1)
      Tests  18 passed (18)
   Start at  01:46:03
   Duration  699ms (transform 63ms, setup 0ms, collect 76ms, tests 7ms, environment 0ms, prepare 226ms)
```

---

## 9. Task 9, and what still fails

### 9.1 A background agent on this project

| Rule | What I require |
| --- | --- |
| Isolation | Use a separate worktree and branch based on `week-10`; never edit the student's active worktree |
| Permitted files | Limit edits to `app/src/App.tsx`, `app/src/booking.ts`, `app/src/booking.test.ts`, and an approved app instruction file |
| Commands | From `app/`, run `npm ci`, `npm test`, and `npm run build`; from `week-10/`, run both Python checks |
| Prohibited actions | Never add credentials, real room data, login/database features, or public deployment configuration |
| Required evidence | Attach the exact diff, test/build output, risk-register updates, and a summary of changed files |
| Before merging or deploying | Require human diff review and passing checks; deployments remain forbidden for this fictional project |

### 9.2 Optional — the deck's checklist prompt (not graded)

Not sent; no second assistant was used.

### 9.3 Checks I am keeping as FAIL or ERROR

| Check | Why it stays |
| --- | --- |
| none | The supplied checker returned no FAIL or ERROR rows |

Process limitation: the Task 2 review did not run in a technically enforced read-only environment,
as stated in §3.1; the checker validates the report structure, not that tool permission.

---

## 10. Release decision and conclusion

**Decision:** CONDITIONAL

CONDITIONAL. R2 was the highest confirmed risk: the original playbook invited real timetable data,
a Supabase login, and a production deploy (9); the approved seven-line patch now forbids those
actions and its A2/A3/C1-C6 checks pass. R1 (6) produced both a validation error and an “Unavailable”
result for reversed times; the new pure helper and R1 regression test now return only the error,
and all 18 tests pass. R3's extra room was removed, and desktop (1280x900) and phone (375x812)
screenshots show the single-room page without clipping. R4 remains: npm audit reports five
advisories in development dependencies; exploitability in this local-only app is unverified. R5
remains partly open because there is no integration test, CI, or lint script. Keep deployment
disabled and review dependencies and add App-level tests before production.
