# AI Usage Disclosure — Week 07

Required by the course academic policy (Generative AI use level **D — AI-integrated**).
You are responsible for the accuracy, testing and integrity of everything you submit,
including anything an AI tool produced.

| Tool | Exact model / plan | Used for | Which files it touched |
| --- | --- | --- | --- |
| Copilot SDK in VS Code | Not displayed | Implemented the first test suite; identified the incorrect T06 expectation | `suites/first/booking.test.ts`, `app/src/booking.test.ts` |
| Copilot SDK in VS Code | Not displayed | Reviewed the first-run failure and drafted the improved test expectation and report text | `app/src/booking.test.ts`, `lab-report.md` |
| Copilot SDK in VS Code | Not displayed | Recreated the starter app, extracted `canBook`, and prepared this disclosure | `app/src/App.tsx`, `app/src/booking.ts`, `app/package.json`, `app/package-lock.json`, `.gitignore`, `AI_USAGE.md` |
| Copilot SDK in VS Code | Not displayed | Ran M2/M3 mutation checks, exercised the page at desktop and mobile widths, and recorded results | `lab-report.md`, `submission.yml`, `evidence/ui-1.png`–`evidence/ui-5.png` |

**I used an assistant to extract `canBook` (Task 1), or to fix a defect in it:** yes
I moved the decision conditions from `starter/src/App.tsx` to `app/src/booking.ts`, preserving their logic. I compared the conditions with the starter source and ran the initial fixed-case suite; its only failure was the incorrect T06 expectation, not a behavior change in the extraction.

**I used another assistant as well (to explain a failure, to draft text in lab-report.md, …):** no — the same assistant also helped explain the T06 failure and draft report text.

**`suites/first/` holds the assistant's first test file exactly as it generated it:** no — the import path was changed to `./booking` when the test was placed in the suite folder.

**Every terminal output in lab-report.md was pasted from a real run, unedited:** yes — the M1–M3 and final test results are from real runs; UI observations are recorded with their screenshots.

**I can explain every test in my final suite — its input, its expected result and the AC behind
it — without the assistant:** Yaroslav to confirm (not answered by the assistant).

**Anything I accepted from the AI without fully understanding it:**
The user should review `app/src/booking.ts` and all expected values in `app/src/booking.test.ts`, especially the strict 120-minute boundary and how invalid existing bookings are treated.

Signed: Yaroslav — confirm before submission
Date: 2026-11-04
