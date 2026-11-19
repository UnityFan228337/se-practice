# AI Usage Disclosure — Week 10

Required by the course academic policy (Generative AI use level **D — AI-integrated**).
You are responsible for the accuracy, testing and integrity of everything you submit,
including anything an AI tool produced.

| Tool | Exact model / plan | Used for | Which files it touched |
| --- | --- | --- | --- |
| GitHub Copilot (Copilot SDK in VS Code) | not displayed | Read-only risk review and report drafting; no app files changed during the review | none during review |
| GitHub Copilot (Copilot SDK in VS Code) | not displayed | Review and draft the approved minimal AGENTS patch | `app/AGENTS.md` |
| GitHub Copilot (Copilot SDK in VS Code) | not displayed | Regression test, availability-feedback mitigation, and one-room correction | `app/src/booking.test.ts`, `app/src/booking.ts`, `app/src/App.tsx` |
| GitHub Copilot (Copilot SDK in VS Code) | not displayed | Prepare the worksheet and declaration | `lab-report.md`, `submission.yml`, `AI_USAGE.md` |

**The review in Task 2 ran in a mode where the assistant could not edit, and `git status` showed no
change afterwards:** no
<!-- The worktree had no app edits during review, but edit tools were available. -->

**I labelled every claim in lab-report.md §3.2 after opening the cited file myself:** yes

**Every change to `app/` was reviewed by me as a diff before I accepted it:** yes
<!-- The assistant reviewed each diff; the student still needs to read and understand them. -->

**I used another assistant as well (to explain a risk, to draft text in lab-report.md, …):** no

**Every terminal output in lab-report.md was pasted from a real run, unedited:** no
<!-- The terminal output came from real runs; trailing whitespace was normalized in the report. -->

**I can explain every score in my register, and why my release decision follows from it, without
the assistant:** no

**Anything I accepted from the AI without fully understanding it:**

The student's independent understanding has not been confirmed. Review the risk scores, pure
helper, and all report claims before submitting.

Signed: Yaroslav
Date: 2026-11-19
