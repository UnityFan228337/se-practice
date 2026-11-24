# AI Usage Disclosure — SIS #05

Required by the course academic policy (Generative AI use level **D — AI-integrated**).
You are responsible for the accuracy, testing and integrity of everything you submit,
including anything an AI tool produced.

| Tool | Exact model / plan | Used for | Which files it touched |
| --- | --- | --- | --- |
| Copilot SDK in VS Code | not displayed | baseline inspection, read-only risk review, and mitigation review | no files in read-only review; later reviewed diffs for project/report files |
| Copilot SDK in VS Code | not displayed | R2 finite-input test and implementation | `project/src/booking.ts`, `project/src/booking.test.ts` |
| Copilot SDK in VS Code | not displayed | R1 dependency audit and upgrade review | `project/package.json`, `project/package-lock.json`, report evidence |

**The risk review ran in a mode where the assistant could not modify files, and `git status` showed
no change afterwards:** yes

**Every finding in report.md §5.2 was labelled after I opened the file or ran the command myself:** yes

**Every change to `project/` was reviewed by me as a diff before I accepted it:** yes
<!-- The R1 package upgrade and R2 finite validation diffs were reviewed before acceptance. -->

**`AGENTS.md`: the assistant loaded it by itself / I pasted it / I did not use it with an assistant:**
I pasted it into the assistant context; this Copilot chat did not load it automatically.

**The weaknesses, the labels, the scores, the decisions and the reflection are my own judgement,
written by me:** yes

**Every output in report.md was pasted from a real run, unedited:** yes

**No real credentials, confidential data or personal data are anywhere in `sis-05/`:** yes

**Anything I accepted from the AI without fully understanding it:**
<!-- The forced dependency upgrade was reviewed for the R1 diff; no change was accepted without understanding the package/test result. -->

Signed: Yaroslav Maltsev
Date: 24 November 2026
