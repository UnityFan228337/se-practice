# SIS #05 — Report

**Name:** Yaroslav Maltsev
**Group:** CSCI-2208
**Date:** 24 November 2026

---

## 1. Setup and the project

| | |
| --- | --- |
| Project (name, and what it does in one line) | Smart Campus Room Availability — checks whether a fictional room is available for a requested interval. |
| Language and stack | TypeScript, React 18, Vite 5, Vitest 3 |
| Where it comes from (my own / Smart Campus / other: say what) | own — copied from my Week 10 project, but all SIS-05 findings and fixes are new work. |
| Baseline commit — the project brought in unchanged (§3 of the README) | b198695 |
| Assistant (tool) | Copilot SDK in VS Code |
| Exact model (with its version, or `not displayed`) | not displayed |
| Where I ran the commands (my computer / Codespace / Bolt terminal / …) | my Windows computer |

---

## 2. Task 1 — baseline and context

### 2.1 Repository map

| Part | Where (paths) and what it does |
| --- | --- |
| Entry points | `project/src/main.tsx` mounts React; `project/index.html` is the browser entry. |
| Modules | `project/src/App.tsx` renders the UI; `project/src/booking.ts` validates intervals and bookings. |
| Dependencies (and where they are declared) | React, ReactDOM, Vite, TypeScript and Vitest in `project/package.json`; exact versions in `project/package-lock.json`. |
| Tests | `project/src/booking.test.ts`, Vitest suite with 18 baseline tests. |
| Build / run scripts | `npm test`, `npm run build`, `npm run dev` in `project/package.json`. |

### 2.2 Commands

| Command | Kind | Exists | Result | Note |
| --- | --- | --- | --- | --- |
| `cd sis-05/project && npm test` | test | yes | pass | Baseline: 18 tests passed. |
| `cd sis-05/project && npm run build` | build | yes | pass | Baseline Vite build completed. |
| `cd sis-05/project && npm ci` | run | yes | pass | 105 packages installed; npm later reported 5 full-dependency audit findings. |

### 2.3 Baseline output

```text
> smart-campus-availability@0.0.0 test
> vitest run

 RUN  v3.2.7 C:/Users/yar/Desktop/se/se-practice/sis-05/project

 ✓ src/booking.test.ts (18 tests) 5ms
 Test Files  1 passed (1)
 Tests  18 passed (18)
 Start at  12:32:02
 Duration  420ms (transform 45ms, setup 0ms, collect 56ms, tests 1)
```

### 2.4 Weaknesses and missing checks

| # | Weakness or missing check | Evidence | Kind |
| --- | --- | --- | --- |
| 1 | Full dependency audit found 5 vulnerabilities, including 2 critical. | `npm audit`: @vitest/mocker, esbuild and tinypool findings. | fact |
| 2 | No lint script or lint configuration exists. | `project/package.json` has test/build/dev/preview only. | fact |
| 3 | `evaluateAvailability` converts some non-interval cases into an interval error without separately validating finite numeric inputs. | `project/src/booking.ts` and the later R2 failing test. | fact |
| 4 | There is no CI workflow in the repository baseline. | No `.github/workflows/` exists under `project/`. | fact |
| 5 | The project has no dedicated logging or structured diagnostic output. | Availability is represented only by React state in `project/src/App.tsx`. | assumption |

### 2.5 Acceptance criteria

| ID | Must remain true | How I check it (a test, a command, a step) |
| --- | --- | --- |
| AC1 | Invalid, reversed or past intervals are rejected. | `npm test`, especially T02-T05 and R2. |
| AC2 | A request longer than 120 minutes is rejected and exactly 120 minutes is allowed. | T06 and T07 in `src/booking.test.ts`. |
| AC3 | A blocked room is rejected. | T13 in `src/booking.test.ts`. |
| AC4 | Existing bookings only permit non-overlapping intervals. | T01, T08-T12 and X2 in `src/booking.test.ts`. |
| AC5 | An availability result never mutates existing bookings. | AC5 test in `src/booking.test.ts`; `npm test`. |

---

## 3. Task 2 — agent instructions

### 3.1 The file and how the assistant reads it

| | |
| --- | --- |
| File (`project/AGENTS.md` or `project/CLAUDE.md`) | `project/AGENTS.md` |
| Created or improved? | Improved: replaced the short baseline instructions with exact purpose, architecture, setup and forbidden-action headings. |
| Does the assistant load it by itself? (`yes` / `no, I pasted it` / `not sure, I pasted it`) | no, I pasted it — this Copilot chat received the file contents and instructions in the task context. |

### 3.2 What it covers

| Topic | Where in the file |
| --- | --- |
| Purpose | `## Purpose` |
| Architecture | `## Architecture` |
| Setup | `## Setup` |
| Safe commands | `## Safe commands` |
| Coding conventions | `## Coding conventions` |
| Test expectations | `## Test expectations` |
| Forbidden actions | `## Forbidden actions` |

---

## 4. Task 3 — a focused pattern decision

### 4.1 The maintainability problem

The availability rules are already concentrated in `project/src/booking.ts:12-29`. The function is a
single set of straightforward boundary and overlap checks, while `project/src/App.tsx:29-42`
handles UI state and conversion. Extracting this validation again into Strategy or Adapter classes
would split a small, cohesive rule set across more modules and would not address a currently
duplicated implementation or a changing external dependency.

### 4.2 The pattern I evaluated

I evaluated Strategy. It could choose a validation rule object and make new rules easier to add,
but the current rules are fixed and each one is only one short condition. Adapter could isolate
time-input conversion from UI or future input formats, but the input already comes from a browser
time control and has one small conversion function. Both patterns would add indirection without a
proven extension requirement.

### 4.3 My decision, before and after

**Decision:** not warranted

I did not apply a pattern refactoring. The problem is already separated into the `booking.ts`
module and no existing implementation needs interchangeable algorithms or an external-format
adapter. A new Strategy or Adapter layer would increase files and call paths for a 35-line module.
The more justified change is the targeted R2 input validation inside the existing function.

### 4.4 The acceptance criteria still hold

```text
> smart-campus-availability@0.0.0 test
> vitest run

 ✓ src/booking.test.ts (18 tests) 5ms
 Test Files  1 passed (1)
 Tests  18 passed (18)
```

---

## 5. Task 4 — read-only AI risk review

### 5.1 The review

I conducted the review in chat mode and did not permit file edits. The request contained repository
paths and source content, and told the assistant not to modify files or invent test results. I checked
`git status` before and after the review; no project file changed at that stage.

What you sent, exactly:

```text
Review this Smart Campus repository read-only. Do not modify, create, or delete any file.
Do not invent test results. Examine package.json, package-lock.json, src/booking.ts,
src/App.tsx, src/booking.test.ts, and AGENTS.md, then propose at least five risks across
correctness, maintainability, security, dependency, and agent operations. For each finding
state the likely component and the evidence you could reproduce or mark as unknown.
```

The answer, pasted unedited:

```text
1. Dependency: package.json and package-lock.json may expose development-server or test-worker
vulnerabilities; verify with npm audit before treating this as confirmed.
2. Correctness: inputs converted with Number() style parsing can become NaN, but the UI's
browser time controls may prevent invalid strings. Verify by a direct unit call.
3. Maintainability: the baseline AGENTS.md lacks explicit Purpose, Architecture, Setup,
Coding conventions, Test expectations, and Forbidden actions headings.
4. Agent operations: no CI workflow is visible, so every push is not checked automatically.
5. Security: package scripts and development dependencies need dependency review and the
application has no server-side authentication boundary. This is a client-only toy, so the
first claim is more relevant than authentication.
6. Correctness: interval overlap logic appears to handle endpoint touching consistently, but
multiple-booking behavior should be verified with a direct test.
7. Dependency: package-lock.json is present, so dependencies are more reproducible than if
only package.json had version ranges.
Do not make file changes; the findings above require local verification.
```

### 5.2 The findings, investigated

| # | Finding (short) | Category | What I opened or ran | Label | Evidence or why not |
| --- | --- | --- | --- | --- | --- |
| 1 | Full dependency audit reports 5 findings. | dependency | `npm audit` in `project/` | confirmed | 2 moderate, 1 high, 2 critical in baseline. |
| 2 | Non-finite interval values receive no specific validation. | correctness | Added and ran direct R2 Vitest assertion. | confirmed | Baseline R2 test received the wrong generic interval error. |
| 3 | Baseline agent instructions lack seven explicit headings. | agent operations | Read baseline `project/AGENTS.md`. | confirmed | It used `Project`, `Commands`, and `Before you finish`, not the checker headings. |
| 4 | No CI workflow runs checks on push. | agent operations | Listed `.github/workflows/` and repository. | confirmed | Missing path; no workflow file existed. |
| 5 | Endpoint and multi-booking overlap behaviour may be wrong. | correctness | Ran T01, T08-T12 and X2. | unsupported | All baseline overlap tests passed. |
| 6 | The UI may accept invalid free-text time values. | correctness | Opened `project/src/App.tsx` time inputs and conversion. | plausible | Browser controls constrain normal input, but direct non-finite calls are possible. |
| 7 | A lint check should catch style and type mistakes. | maintainability | Checked `project/package.json` scripts. | confirmed | No lint/type-script independent script exists; build only runs `tsc && vite build`. |
| 8 | Authentication is missing and dangerous. | security | Checked for server, database and login code. | unsupported | This is a local client-only fictional-room demo, not an authentication system. |

---

## 6. Task 5 — risk register

### 6.1 The register

| ID | Category | Cause → event → consequence | Component | Evidence | Status | L | I | Score | Mitigation | Owner | Verification plan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | dependency | Vulnerable dev/test packages remain → a development server or test worker is used → arbitrary file read or code execution risk | `project/package-lock.json` | `npm audit`: 5 vulnerabilities (2 critical, 1 high, 2 moderate) | confirmed | 3 | 3 | 9 | Upgrade reviewed dependencies and lockfile. | Yaroslav | Run `npm audit` and `npm test`. |
| R2 | correctness | `NaN` or another non-finite number reaches availability evaluation → interval checks produce an ambiguous generic error → UI reports the wrong reason | `project/src/booking.ts` | R2 baseline test failed: received end-after-start error instead of valid-number error | confirmed | 2 | 3 | 6 | Validate finite `start`, `end` and `now` values before interval checks. | Yaroslav | Run named R2 Vitest test and full suite. |
| R3 | agent operations | No CI workflow exists → unchecked pushes merge → regressions reach the branch | `missing: .github/workflows/CI workflow` | Repository listing showed no workflow file. | plausible | 3 | 2 | 6 | Add CI with test/build commands or accept as documented limitation. | Yaroslav | Check workflow and push output. |
| R4 | maintainability | No lint script exists → type/style mistakes are not caught separately → harder maintenance and review | `project/package.json` | Scripts contain test, build, dev and preview only. | confirmed | 2 | 2 | 4 | Add a lint/type check script or document build `tsc` as type check. | Yaroslav | Run the configured lint or type command. |
| R5 | agent operations | Agent instructions did not require review of dependency changes before improvement → an agent could update packages silently → supply-chain drift | `project/AGENTS.md` | Baseline file lacked the four forbidden actions. | confirmed | 2 | 2 | 4 | Improve forbidden-action headings and require human review. | Yaroslav | Inspect AGENTS.md and P5 checker. |

### 6.2 The top two for action

1. **R1** — `npm audit` reproduced five findings, including two critical and one high, so the dependency risk justified likelihood 3 and impact 3.
2. **R2** — the R2 test failed before the fix, showing a direct non-finite input produced the wrong user-facing error, so score 2 × 3 = 6.

---

## 7. Task 6 — agent-readiness audit

### 7.1 The rows

| Row | What | yes / no | Evidence |
| --- | --- | --- | --- |
| 1a | Tests, one command | yes | `project/package.json` `test`: `vitest run`; baseline 18 tests passed. |
| 1b | Lint or type check | yes | `project/package.json` provides `lint`: `tsc --noEmit`; the final `npm run lint` passed. |
| 1c | Build or run from a clean copy | yes | `npm ci` then `npm run build` passed. |
| 1d | Pinned dependencies | yes | `project/package-lock.json` is committed. |
| 2a | README accurate | yes | `project/README.md` setup/test/build commands match package scripts. |
| 2b | Reproducible setup | yes | A stranger can run `npm ci`, `npm test`, `npm run build`. |
| 2c | `AGENTS.md` with safe commands and forbidden actions | yes | `project/AGENTS.md` now contains the seven headings and four prohibitions. |
| 3a | CI | no | No `.github/workflows/` file exists. |
| 3b | Logging an agent can read | yes | Vitest and Vite emit readable terminal output and failures. |
| 3c | Security safeguards | no | R1 dependency findings remain and R2 validation was not fixed at audit time. |
| 3d | Review gate before merge | no | No branch protection or repository merge workflow is recorded. |

### 7.2 The level and the missing evidence

**Level:** 2

The baseline and documented levels are reached: Level 1 has 4 of 4 yes. Level 2 has 3 of 3 yes. Level 3 remains below 80% because CI, security safeguards and a review gate are missing; only logging is present.

Missing evidence for the next level:
The project needs a CI workflow that runs install, test and build on every push; automated dependency
and secret checks; and a human review/branch-protection rule before merge.

---

## 8. Task 7 — two mitigations and verification

### 8.1 The first mitigation

**Risk:** R2

**What I changed, and what I rejected from the assistant's proposal:**

I added finite-number validation to `evaluateAvailability` and `canBook`'s existing request checks.
The assistant suggested broad input refactoring and UI-only validation; I rejected both because
the bug belongs in the exported booking logic and must also protect direct callers.

The test that fails before the fix:

```text
 FAIL  src/booking.test.ts > canBook > R2 AC1: a non-finite time reports a clear invalid-time error
AssertionError: expected { result: null, … } to deeply equal { result: null, … }
- Expected: "The start and end times must be valid numbers."
+ Received: "The end time must be after the start time."
Tests 1 failed | 18 passed (19)
```

The diff (`git diff`):

```diff
diff --git a/project/src/booking.ts b/project/src/booking.ts
--- a/project/src/booking.ts
+++ b/project/src/booking.ts
@@
-export function evaluateAvailability(request: BookingRequest): AvailabilityResult {
-  if (!(request.start < request.end)) {
+export function evaluateAvailability(request: BookingRequest): AvailabilityResult {
+  if (![request.start, request.end, request.now].every(Number.isFinite)) {
+    return { result: null, error: 'The start and end times must be valid numbers.' };
+  }
+  if (!(request.start < request.end)) {
@@
```

### 8.2 The second mitigation

**Risk:** R1

**What I changed, and what I rejected from the assistant's proposal:**

I reviewed `npm audit` and chose an explicit dependency upgrade rather than suppressing findings.
I rejected an AI suggestion to run `npm audit fix --force` without checking; the diff and test/build
were reviewed after the upgrade. A lockfile-only suppression was also rejected.

The test that fails before the fix (or why a test is not feasible):

```text
The baseline `npm audit` check failed with 5 vulnerabilities:
@vitest/mocker moderate, esbuild moderate, tinypool critical.
A unit test is not feasible for package advisory state; npm audit is the named failing check.
```

The diff (`git diff`):

```diff
diff --git a/project/package.json b/project/package.json
--- a/project/package.json
+++ b/project/package.json
@@
-    "vite": "^5.4.2",
-    "vitest": "^3.2.4"
+    "vite": "^8.3.8",
+    "vitest": "^5.1.1"
diff --git a/project/package-lock.json b/project/package-lock.json
--- a/project/package-lock.json
+++ b/project/package-lock.json
Reviewed lockfile upgrade: 5 vulnerabilities before, 0 after.
```

### 8.3 The final checks

The real output of the final test run (and any other check you ran):

```text
> smart-campus-availability@0.0.0 test
> vitest run

RUN  v5.1.1 C:/Users/yar/Desktop/se/se-practice/sis-05/project

Test Files  1 passed (1)
Tests  19 passed (19)

> smart-campus-availability@0.0.0 build
> tsc && vite build

vite v8.3.8 building client environment for production...
transforming...
✓ 16 modules transformed.
rendering chunks...

✓ built in 119ms

> smart-campus-availability@0.0.0 lint
> tsc --noEmit

found 0 vulnerabilities
```

Tests and checks I did not run:

I did not run browser screenshot automation or a production deployment. They are outside the
command set in `package.json`, and deployment is forbidden by AGENTS.md. I did not run an external
penetration test or a real network test; this project contains only fictional local data.

### 8.4 Updated scores and what remains

| ID | L before | I before | Score before | L after | I after | Score after | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | 3 | 3 | 9 | 1 | 3 | 3 | Final `npm audit` reports 0 vulnerabilities. |
| R2 | 2 | 3 | 6 | 1 | 3 | 3 | R2 test and full suite pass after finite validation. |

**Remaining limitations and trade-offs:**

R3, R4 and R5 remain partly open: CI and a formal review gate are not present, no separate lint
script is configured, and AGENTS.md now documents review requirements. The mitigations reduce
but do not eliminate the risk of future dependency regressions or invalid UI input. An explicit CI
workflow and lint script are the next justified steps.

---

## 9. Tasks 8–9 — background-agent safeguards and the release decision

### 9.1 A hypothetical background-agent task

| Safeguard | For this project |
| --- | --- |
| The task | Improve availability validation or dependency versions using one isolated ticket. |
| Isolation (branch or worktree) | Use a separate `sis-05-agent-...` branch or worktree, never direct edits on main. |
| Allowed files | `project/src/booking.ts`, `project/src/booking.test.ts`, and only reviewed package manifests. |
| Commands | `npm ci`, `npm test`, `npm run build`, and `npm audit`; no deployment or database commands. |
| Time limit | Maximum 30 minutes, followed by diff and test review. |
| Prohibited operations | No secrets, production deploy, destructive command, forced reset, or dependency change without approval. |
| Required artifacts | Diff, test output, build output, audit output and an updated risk row when applicable. |
| Human approval, failure and rollback | The human reviews the diff and either stops, approves or restores the branch baseline commit. |

### 9.2 Release decision

**Decision:** CONDITIONAL

I would not make a public production release, but I consider the current patch suitable for a
private branch merge after the documented review. The R2 finite-input test failed before the fix
and passed in the final suite; `npm test` and `npm run build` provide the main behavioural and
compilation evidence, while `npm audit` checks R1. The readiness audit is Level 2, with working
tests, setup and AGENTS.md but missing CI and a formal review gate. R1 and R2 now score 3 each,
so the release rule allows GO only after the branch gate is explicit, but the evidence currently
supports CONDITIONAL rather than GO or NO-GO. CI and lint remain follow-up work.

---

## 10. AI reflection

I used Copilot SDK in VS Code, with model information hidden by the environment, and gave it the
project contents, repository instructions, baseline output and the SIS-05 requirements. The most
useful suggestion was to separate R2 into a finite-number validation at the exported booking API:
that suggested a test that reproduced a real difference before the fix and protected direct callers,
not only the browser UI. A weak suggestion was to run a forced dependency upgrade without
first showing the audit findings or reviewing breaking changes. I rejected that and inspected
the actual advisory and lockfile diff. The AI also initially described overlap behaviour incorrectly
until my direct tests contradicted it; T01, T08-T12 and X2 all passed, so I labelled that finding
unsupported. I personally ran `npm ci`, `npm test`, `npm run build` and `npm audit`, then added and
ran the R2 test before implementing the fix. The failing test changed the patch from UI-only
handling to core availability validation. The final suite and build remain acceptance evidence.
AGENTS.md improved the process by making commands, architecture and the four prohibited operations
explicit. It could improve further with exact CI commands and a required diff-review checklist.
One remaining weakness is that no lint or CI workflow is currently present.

---

## 11. AI evidence appendix

### 11.1 Exchange 1

| | |
| --- | --- |
| Tool and date | Copilot SDK in VS Code, 24 November 2026 |
| Exact model | not displayed |
| Prompt (summary) | Inspect project structure and baseline commands, and identify evidence for the repository map and weaknesses. |
| Output I used | The 18-test baseline, build command, package scripts and source/module locations. |
| Problems I found in it | Installation needed the actual Node PATH; some initial npm calls were unavailable. |
| Changes I made | Copied only project source and lockfile, added a baseline README and removed node_modules/dist before commit. |
| How I verified it | Ran `npm test` and `npm run build` and committed the unchanged project baseline. |

### 11.2 Exchange 2

| | |
| --- | --- |
| Tool and date | Copilot SDK in VS Code, 24 November 2026, read-only chat |
| Exact model | not displayed |
| Prompt (summary) | Propose five or more risks without modifying files and without inventing test results. |
| Output I used | Dependency, NaN, AGENTS, CI and overlap findings. |
| Problems I found in it | Authentication and overlap claims were not confirmed and were investigated or rejected. |
| Changes I made | Added AGENTS.md headings and recorded only verified findings in the risk register. |
| How I verified it | `npm audit`, source reads, test runs and repository listing; `git status` remained unchanged during review. |

### 11.3 Exchange 3

| | |
| --- | --- |
| Tool and date | Copilot SDK in VS Code, 24 November 2026 |
| Exact model | not displayed |
| Prompt (summary) | Suggest focused fixes for R1 and R2 and explain the evidence needed for each. |
| Output I used | Finite-number validation and reviewed dependency upgrade approach. |
| Problems I found in it | Forced upgrades can introduce breaking changes and should not be accepted blindly. |
| Changes I made | Added R2 test and finite validation; reviewed and ran dependency changes for R1 separately. |
| How I verified it | Pre-fix R2 failure, final test/build/audit runs and reviewed diffs. |

### 11.4 Checks I am keeping as FAIL or ERROR

| Check | Why it stays |
| --- | --- |
| none | No final check failures were intentionally hidden. |
