# Lab report — Practice #02: The Prompt Is an Engineering Input

**Name: Мальцев Ярослав**
**Group: [CSCI-2208] Software Engineering - Fall 2026  16:00-19:00**
**Date: **

> Fill in every section. **Do not delete or renumber the headings** — the grading pass reads them
> by number. If something did not happen, write "did not happen" and why; an empty section and a
> fabricated one are graded the same way.

---

## 1. The frozen experiment

| | |
| --- | --- |
| AI assistant | Gemini |
| Exact model name | Gemini 3.6 Flash |
| Implementation language | Python |
| Date of the runs | 17.09 |

<!-- **Non-Python students only** — paste your substituted Prompt B text here, so the substitution can
be checked:

```
(paste here, or write "n/a — used Python")
``` -->

**Confirmations:**

- Each prompt was sent in a **fresh chat**: yes
- No follow-up questions were asked before Part 7: yes / no
- Every output was saved **before** any editing: yes / no

---

## 2. Prompt A — minimal

**Prompt sent** (should be exactly one sentence):

```
Write Python code to analyze student marks.

```

**Assumptions the AI made that I never gave it** — list them, one per line. A data format, a pass
threshold, a rounding rule, an input method, an invented feature all count.

1. Using numpy library
2. Using pandas library
3. I dont give a student data
4. Gemini make table of subjects, and made fictional subjects


**Questions it should have asked and did not:**

1. Data
2. Input format
3. May he use a libraries
4. Is it only for one subjects or for many

**Is the function named `analyze_marks` with the required signature?** yes

**First impression before testing** (one sentence — you will compare this with section 6 later):
Not bad, a lot of code, difficult architecture for that small application.
---

## 3. Prompt B — structured context

**Prompt sent** (paste it in full, including any substitutions):

```
You are a Python developer. Implement analyze_marks(marks, pass_mark=50). Return
average, highest, lowest, and pass_rate in a dictionary. Accept marks from 0 to 100;
raise ValueError for an empty list, non-numeric values, or out-of-range values. Use
no external libraries. Return code plus a short explanation.

```

**What B fixed compared to A:**

1. Dont make big and difficult architecture
2. Dont fake up a new subjects, he calculate it for one

**What B still leaves open:**

1. Dont make an input
2. 

---

## 4. Prompt C — examples and tests

**What I appended to Prompt B:**

```
Example: analyze_marks([40, 60, 80], 50) → average 60, highest 80, lowest 40,
pass_rate 66.67. Include tests for: one mark, decimals, custom pass_mark, empty list,
text value, and marks below 0 or above 100. State any remaining assumptions before
the code.

```

**Tests the AI wrote for itself** — how many, and which situations do they cover?
7
1. 75
2. 45.5 60.5 84
3. 40 60 80 pass_mark = 70
4. empty
5. 50 "eighty" 90
6. 50 -10 80
7. 50 105 80 

| Situation | Covered by the AI's tests? |
| --- | --- |
| one mark | yes |
| decimals | yes |
| custom pass_mark | yes |
| empty list | yes |
| text value | yes |
| below 0 / above 100 | yes |

**Do the AI's own tests pass against the AI's own code?** yes

**Do they agree with the harness in section 6?** yes

**Assumptions C stated explicitly before the code:**

---

## 5. Prompt D — my combined prompt

**The complete prompt I wrote** (one message, sent to a fresh chat):

```
You are a Python developer. Implement analyze_marks(marks, pass_mark=50). Return
average, highest, lowest, and pass_rate in a dictionary. Accept marks from 0 to 100;
raise ValueError for an empty list, non-numeric values, or out-of-range values. Use
no external libraries. Return code plus a short explanation.

Example: analyze_marks([40, 60, 80], 50) → average 60, highest 80, lowest 40,
pass_rate 66.67. Include tests for: one mark, decimals, custom pass_mark, empty list,
text value, and marks below 0 or above 100. State any remaining assumptions before
the code.

there are test for knowing
#CallRequiredABCD1analyze_marks([40, 60, 80], 50)avg 60 · high 80 · low 40 · rate 66.672analyze_marks([100], 50)avg 100 · high 100 · low 100 · rate 1003analyze_marks([49.5, 50], 50)avg 49.75 · high 50 · low 49.5 · rate 504analyze_marks([], 50)raises ValueError5analyze_marks([40, "60"], 50)raises ValueError6analyze_marks([-1, 50, 101], 50)raises ValueError

Add an input for marks

```

**What I deliberately added that A, B and C did not have:**

1. Input for marks
2. Tests for app

**The ambiguity I found in the specification, and how I resolved it inside Prompt D:**

---

## 6. Test results — the evidence

Six cases × four prompts. Verdicts are **PASS**, **FAIL** or **ERROR** only.

| # | Call | Required | A | B | C | D |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `analyze_marks([40, 60, 80], 50)` | avg 60 · high 80 · low 40 · rate 66.67 | **ERROR** | **PASS** | **PASS** | **PASS** |
| 2 | `analyze_marks([100], 50)` | avg 100 · high 100 · low 100 · rate 100 | **ERROR** | **PASS** | **PASS** | **PASS** |
| 3 | `analyze_marks([49.5, 50], 50)` | avg 49.75 · high 50 · low 49.5 · rate 50 | **ERROR** | **PASS** | **PASS** | **PASS** |
| 4 | `analyze_marks([], 50)` | raises ValueError | **ERROR** | **PASS** | **PASS** | **PASS** |
| 5 | `analyze_marks([40, "60"], 50)` | raises ValueError | **ERROR** | **PASS** | **PASS** | **PASS** |
| 6 | `analyze_marks([-1, 50, 101], 50)` | raises ValueError | **ERROR** | **PASS** | **PASS** | **PASS** |
| | **Totals** | | 6/6 | 6/6 | 6/6 | 6/6 |

**For every FAIL and ERROR above, one line: what was returned or raised instead.**

| Prompt | Case | What actually happened |
| --- | --- | --- |
| Write Python code to analyze student marks. | 1 | raised TypeError: analyze_marks() takes 1 positional argument but 2 were given |
| Write Python code to analyze student marks. | 2 | raised TypeError: analyze_marks() takes 1 positional argument but 2 were given |
| Write Python code to analyze student marks. | 3 | raised TypeError: analyze_marks() takes 1 positional argument but 2 were given |
| Write Python code to analyze student marks. | 4 | raised TypeError instead of ValueError: analyze_marks() takes 1 positional argument but 2 were given |
| Write Python code to analyze student marks. | 5 | raised TypeError instead of ValueError: analyze_marks() takes 1 positional argument but 2 were given |
| Write Python code to analyze student marks. | 6 | raised TypeError instead of ValueError: analyze_marks() takes 1 positional argument but 2 were given |

### Pasted terminal output — all four runs

> This is the part that makes the table above count. Paste the **whole** output, unedited,
> including the header lines. A table with nothing behind it is not accepted.

**Prompt A**

```
========================================================================
analyze_marks harness — code/prompt_a.py
tolerance for numeric comparison: 0.01
========================================================================
SIGNATURE: ok
------------------------------------------------------------------------
case 1  ERROR  analyze_marks([40, 60, 80], 50)
          expect: average=60.0, highest=80, lowest=40, pass_rate=66.67
          got   : raised TypeError: analyze_marks() takes 1 positional argument but 2 were given
------------------------------------------------------------------------
case 2  ERROR  analyze_marks([100], 50)
          expect: average=100.0, highest=100, lowest=100, pass_rate=100.0
          got   : raised TypeError: analyze_marks() takes 1 positional argument but 2 were given
------------------------------------------------------------------------
case 3  ERROR  analyze_marks([49.5, 50], 50)
          expect: average=49.75, highest=50, lowest=49.5, pass_rate=50.0
          got   : raised TypeError: analyze_marks() takes 1 positional argument but 2 were given
------------------------------------------------------------------------
case 4  ERROR  analyze_marks([], 50)
          expect: ValueError
          got   : raised TypeError instead of ValueError: analyze_marks() takes 1 positional argument but 2 were given
------------------------------------------------------------------------
case 5  ERROR  analyze_marks([40, '60'], 50)
          expect: ValueError
          got   : raised TypeError instead of ValueError: analyze_marks() takes 1 positional argument but 2 were given
------------------------------------------------------------------------
case 6  ERROR  analyze_marks([-1, 50, 101], 50)
          expect: ValueError
          got   : raised TypeError instead of ValueError: analyze_marks() takes 1 positional argument but 2 were given
------------------------------------------------------------------------
RESULT  0 PASS · 0 FAIL · 6 ERROR   (code/prompt_a.py)
========================================================================
```

**Prompt B**

```
========================================================================
analyze_marks harness — code/prompt_b.py
tolerance for numeric comparison: 0.01
========================================================================
SIGNATURE: ok
------------------------------------------------------------------------
case 1  PASS   analyze_marks([40, 60, 80], 50)
          expect: average=60.0, highest=80, lowest=40, pass_rate=66.67
          got   : average=60.0, highest=80, lowest=40, pass_rate=66.66666666666666
------------------------------------------------------------------------
case 2  PASS   analyze_marks([100], 50)
          expect: average=100.0, highest=100, lowest=100, pass_rate=100.0
          got   : average=100.0, highest=100, lowest=100, pass_rate=100.0
------------------------------------------------------------------------
case 3  PASS   analyze_marks([49.5, 50], 50)
          expect: average=49.75, highest=50, lowest=49.5, pass_rate=50.0
          got   : average=49.75, highest=50, lowest=49.5, pass_rate=50.0
------------------------------------------------------------------------
case 4  PASS   analyze_marks([], 50)
          expect: ValueError
          got   : raised ValueError: The marks list cannot be empty.
------------------------------------------------------------------------
case 5  PASS   analyze_marks([40, '60'], 50)
          expect: ValueError
          got   : raised ValueError: All marks must be numeric. Found invalid value: 60
------------------------------------------------------------------------
case 6  PASS   analyze_marks([-1, 50, 101], 50)
          expect: ValueError
          got   : raised ValueError: Marks must be between 0 and 100. Found out-of-range value: -1
------------------------------------------------------------------------
RESULT  6 PASS · 0 FAIL · 0 ERROR   (code/prompt_b.py)
========================================================================

```

**Prompt C**

```

========================================================================
analyze_marks harness — code/prompt_c.py
tolerance for numeric comparison: 0.01
========================================================================
SIGNATURE: ok
------------------------------------------------------------------------
case 1  PASS   analyze_marks([40, 60, 80], 50)
          expect: average=60.0, highest=80, lowest=40, pass_rate=66.67
          got   : average=60.0, highest=80, lowest=40, pass_rate=66.66666666666666
------------------------------------------------------------------------
case 2  PASS   analyze_marks([100], 50)
          expect: average=100.0, highest=100, lowest=100, pass_rate=100.0
          got   : average=100.0, highest=100, lowest=100, pass_rate=100.0
------------------------------------------------------------------------
case 3  PASS   analyze_marks([49.5, 50], 50)
          expect: average=49.75, highest=50, lowest=49.5, pass_rate=50.0
          got   : average=49.75, highest=50, lowest=49.5, pass_rate=50.0
------------------------------------------------------------------------
case 4  PASS   analyze_marks([], 50)
          expect: ValueError
          got   : raised ValueError: The marks list cannot be empty.
------------------------------------------------------------------------
case 5  PASS   analyze_marks([40, '60'], 50)
          expect: ValueError
          got   : raised ValueError: Invalid value '60'. All marks must be numeric.
------------------------------------------------------------------------
case 6  PASS   analyze_marks([-1, 50, 101], 50)
          expect: ValueError
          got   : raised ValueError: Mark -1 is out of range. Must be between 0 and 100.
------------------------------------------------------------------------
RESULT  6 PASS · 0 FAIL · 0 ERROR   (code/prompt_c.py)
========================================================================

```

**Prompt D**

```
========================================================================
analyze_marks harness — code/prompt_d.py
tolerance for numeric comparison: 0.01
========================================================================
SIGNATURE: ok
------------------------------------------------------------------------
case 1  PASS   analyze_marks([40, 60, 80], 50)
          expect: average=60.0, highest=80, lowest=40, pass_rate=66.67
          got   : average=60.0, highest=80, lowest=40, pass_rate=66.67
------------------------------------------------------------------------
case 2  PASS   analyze_marks([100], 50)
          expect: average=100.0, highest=100, lowest=100, pass_rate=100.0
          got   : average=100.0, highest=100, lowest=100, pass_rate=100.0
------------------------------------------------------------------------
case 3  PASS   analyze_marks([49.5, 50], 50)
          expect: average=49.75, highest=50, lowest=49.5, pass_rate=50.0
          got   : average=49.75, highest=50, lowest=49.5, pass_rate=50.0
------------------------------------------------------------------------
case 4  PASS   analyze_marks([], 50)
          expect: ValueError
          got   : raised ValueError: The marks list cannot be empty.
------------------------------------------------------------------------
case 5  PASS   analyze_marks([40, '60'], 50)
          expect: ValueError
          got   : raised ValueError: Invalid mark '60': All marks must be numeric (int or float).
------------------------------------------------------------------------
case 6  PASS   analyze_marks([-1, 50, 101], 50)
          expect: ValueError
          got   : raised ValueError: Invalid mark '-1': Marks must be between 0 and 100.
------------------------------------------------------------------------
RESULT  6 PASS · 0 FAIL · 0 ERROR   (code/prompt_d.py)
========================================================================
```

---

## 7. Scoring

0–2 per criterion, using the rubric in `README.md` Part 7.

| Criterion | A | B | C | D |
| --- | --- | --- | --- | --- |
| Correctness (cases passed) | 0 | 2 | 2 | 2 |
| Requirement coverage | 1 | 2 | 2 | 2 |
| Verifiability (tests) | 0 | 1 | 2 | 2 |
| Assumptions stated | 0 | 1 | 2 | 2 |
| Noise (2 = none) | 0 | 2 | 2 | 2 |
| **Total / 10** | 1 | 8 | 10 | 10 |

**Prompt length, in words:** A ____ · B ____ · C ____ · D ____

**Words added per point gained** — B over A, C over B, D over C. One line on what that ratio says:

---

## 8. Conclusion — 150–200 words

Answer in this order: (1) which prompt scored best, and whether it is the one you would actually
use at work; (2) which single addition bought the most correctness, naming the exact case that
changed verdict; (3) what was pure noise; (4) the ambiguity and your resolution.

Name test cases and real returned values. "More detailed prompts work better" scores zero.

```
(150–200 words)
1. Prompt D and Prompt C got the best score (10/10). But I would use Prompt D at work because it stops the AI from guessing rules.

2. Adding clear rules for errors bought the most correctness. In Prompt A, the code crashed on bad inputs. Adding requirements to raise a ValueError for empty lists, text, or numbers outside 0–100 fixed this. Specifically, Case 4 (analyze_marks([], 50)), Case 5 (analyze_marks([40, "60"], 50)), and Case 6 (analyze_marks([-1, 50, 101], 50)) changed from **ERROR** in Prompt A to **PASS** in B, C, and D.

3. Prompt A added pure noise. Instead of writing just one function, it wrote extra code for CLI menus, file reading, and custom print statements.

4. The main unclear rule was how to round pass_rate. Standard division for [40, 60, 80] gives 66.66666666666667 instead of 66.67. I fixed this in Prompt D by writing: "Calculate pass_rate as a percentage rounded to 2 decimal places using round(..., 2)".


```

**Word count: 175**

---

## 9. Two questions for the debrief

Written before class, answered in class.

1. How to write prompt, that make application better, and spend less tokens
