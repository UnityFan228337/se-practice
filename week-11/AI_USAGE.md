# AI Usage Disclosure - Week 11

| Tool | Exact model / plan | Used for | Which files it touched |
| --- | --- | --- | --- |
| GitHub Copilot in VS Code | not displayed | feature, mock adapter, explain.ts, button and tests | booking.ts, explain.ts, explain.test.ts, App.tsx, index.css |
| GitHub Copilot in VS Code | not displayed | three prompt variants and the comparison | none |
| VS Code code-review agent | not displayed | read-only agentic review | none |
| GitHub Copilot in VS Code | not displayed | the V1 and V2 fixes | explain.ts, explain.test.ts |

**Every file the assistant changed in Task 3 was reviewed by me before I accepted it (§4.2):** yes

**No API key, token or provider call is anywhere in `app/src/`:** yes

**The review in Task 6 ran in a mode where the assistant could not edit, and `git status` showed no
change afterwards:** yes

**I labelled every finding in §7.3 after verifying it myself:** yes

**I used another assistant as well (to explain an error, to draft text in lab-report.md, …):** no

**Every terminal output in lab-report.md was pasted from a real run, unedited:** yes

**I can explain how explainAvailability handles a timeout and a contradicting answer, without the
assistant:** yes

**Anything I accepted from the AI without fully understanding it:** none

Signed: Maltsev Yaroslav
Date: 24 November 2026
