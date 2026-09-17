# Week 01 — Manual vs AI: Comparison

**Name:** Мальцев Ярослав
**Group:** [CSCI-2208] Software Engineering - Fall 2026 16:00-19:00
**Date:** 12.09

---
I cant download.<br/>
LINK: https://marksanalyzer-lqt570.public.builtwithrocket.new/
---

## 1. Facts

| | Manual (Part 1) | Rocket (Part 2) |
| --- | --- | --- |
| Language / stack used | Python | Next.js and TypeScript |
| Time to first version that ran | 10 | 5 |
| Time to all 4 test cases passing | 12 | 5 |
| Number of attempts / prompts needed | 3 | 1 |
| Lines of code you actually wrote | 31 | 0 |
| Did it handle invalid marks (case B)? | yes | yes |
| Did it handle an empty list (case D)? | yes | yes |
| Did it use the ≥ 50 pass threshold? | yes | yes |
| Output format matches the spec? | yes | yes |
| Can you explain every line of it? | yes  | yes |

## 2. Test results

| Case | Input | Manual output | Rocket output | Spec says | Match? |
| --- | --- | --- | --- | --- | --- |
| A | `85, 23, 45, 90, 92` | | | avg 67.00 · high 92 · low 23 · pass 60.0% | yes |
| B | `88, 47, -5, 101, abc, 73, 50, , 100` | | | avg 71.60 · high 100 · low 47 · pass 80.0% | yes |
| C | `10, 20, 30` | | | avg 20.00 · high 30 · low 10 · pass 0.0% | yes |
| D | `abc, , xyz` | | | clear message, no crash | yes |

## 3. What the AI added that I never asked for

<!-- Tech stack, UI, extra features, a pass threshold it invented, styling, etc. -->

- Build an app on Node.js
- UI
- Button "Copy"
- Button "Reset"

## 4. What the AI got wrong or silently skipped

<!-- Be concrete: input, expected, actual. -->

- Dont get a point to "one line - one student"

## 5. The defect I asked Rocket to fix

**Prompt I used:** On the next line is other student, and have to be his own statistics



**Result:** (fixed)

**What this tells me:**

--- How accuracy prompt, that accuracy result

## 6. Reflection (200–300 words)

Answer all four, in your own words:

1. Which parts of the work did the AI genuinely speed up?
2. Where did the AI cost you time, or give you something that looked right but was not?
3. Which of these two artefacts would you be willing to put your name on, and why?
4. What must a human engineer still be responsible for after this experiment?

<!-- Write your reflection below this line -->



<br/>
<br/>
<br/>
<br/>
<br/>

1. The AI genuinely speed up the initial project setup and frontend layout creation. Instead of spending time configuring a UI framework, or styling form inputs and card layouts, rocket.new built a functional web interface in under 5 minutes. It instantly handled  basic input that would have taken much longer to create manually.

2. However, the AI cost time by adding unrequested features and missing exact formatting constraints. Rather than writing a lean script, it generated a full web application packed with extra statistics—like median and standard deviation and interactive widgets. It also dont get a point about one line - one student, it requires me an extra prompt to fix it.

3. I would be willing to put my name on the manual Python solution. Because I wrote every line myself, I understand its execution flow, input validation. The Rocket artifact looks strange, but submitting an entire generated web stack introduces unnecessary complexity, unverified dependencies, and code I did not write from scratch.

4. Human engineer remains responsible for system requirements, edge-case verification, and overall code integrity. While AI can build solutions quickly, only a human developer can ensure strict specification compliance, audit logic for silent errors, and take full responsibility for what gets deployed.