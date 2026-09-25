# Lab report — Practice #03, Requirements Engineering with AI

Fill in every section. **Do not delete or renumber the headings** — the README points at them and a
missing heading reads as a missing section.

Name: Мальцев Ярослав
Student ID: 25B030214
GitHub username: UnityFan228337

---

## 1. Setup

| | |
| --- | --- |
| AI assistant (tool) | Gemini |
| Exact model name and version | Gemini 3.6 Flash |
| Date of the session | 23.09 |
| Diagram renderer used | https://plantuml.com/ |

One tool and one model for all three prompts. If you switched, say why here — it changes what your
findings mean.

---

## 2. Original AI output — user stories (Part 1)

Paste the **unedited** response to Prompt 1. Do not tidy it. If it is long, paste all of it anyway;
this is the baseline everything else is measured against.

```
As a Student, I want to check which study rooms are available at specific times, so that I can schedule my study sessions effectively.
Priority: High
Assumption: Room schedules update instantly across all user views.

As a Student, I want to reserve an open room for my group, so that we have a designated room to work in.
Priority: High
Assumption: The student possesses a valid campus ID.

As a Student, I want to cancel my reservation if my plans change, so that other students can use the room.
Priority: Medium
Assumption: Cancellations can be made up to the start time.

As an Administrator, I want to temporarily block a room for maintenance, so that students do not book broken spaces.
Priority: High
Assumption: Maintenance status is visible to all students immediately.

As an Administrator, I want to unblock a room after maintenance, so that it enters the available pool again.
Priority: Medium
Assumption: Unblocking resets default availability parameters.

As an Administrator, I want to view room booking statistics, so that I can report library usage to management.
Priority: Low
Assumption: Statistics include total hours booked and room occupancy rates.

As a System, I want to send confirmation notifications to students, so that they have proof of booking.
Priority: High
Assumption: Email/notification channels are operational.
```

---

## 3. Story review (Part 2)

One row per change you made. "Kept unchanged" is a valid row and needs a reason too.

One row per change you made. "Kept unchanged" is a valid row and needs a reason too.

| Story (as generated) | What I did | Why | Final ID |
| --- | --- | --- | --- |
| As a Student, I want to view room availability for specific time slots, so that I can find an open study space for my schedule. | Kept unchanged | Valid stakeholder (Student), clear outcome, aligns with UC-01. | US-01 |
| As a Student, I want to book an available study room for a future time slot, so that I have a guaranteed place to study. | Revised wording | Refined goal to single or group study staying within scope. | US-02 |
|  As a Student, I want to cancel my existing room booking, so that the room becomes available for other students if I no longer need it. | Kept unchanged | Valid stakeholder, clear benefit, aligns with UC-03. | US-03 |
| As an Administrator, I want to block a study room from being booked, so that students cannot reserve it. | Kept unchanged | Valid stakeholder (Administrator), aligns with UC-04 block logic. | US-04 |
| As an Administrator, I want to unblock a previously blocked room, so that it becomes available for student reservations again. | Kept unchanged | Valid stakeholder (Administrator), aligns with UC-04 unblock logic. | US-05 |
| As an Administrator, I want to review room usage metrics over selected time periods, so that I can understand peak hours and optimize library room allocation. | Revised wording | Removed "management reporting" scope, aligned with UC-05 Review usage. | US-06 |
| As a Student, I want to receive an automated notification confirming my booking or cancellation action, so that I have written proof of my reservation status. | Rewrote role | AI used "System" as role; changed to "Student" who wants notification. | US-07 |

**Did the assistant invent anything outside the scenario?**
No out-of-scope items (e.g., payments, QR codes, authentication) were introduced. However, the AI attempted to assign "System" as a stakeholder role in Story 7, which violates the strict stakeholder definitions (Student and Administrator only).

**How many stories did you end with, and why that number?**
Ended with 7 stories. This number provides exact coverage for all six mandatory use cases (UC-01 to UC-06), explicitly splitting block/unblock into two clear administrator stories (US-04 and US-05) and assigning a proper student goal to notifications (US-07).

---
**Did the assistant invent anything outside the scenario?** QR-code for rooms, database and dashboards to see peak usage and popular room types

**How many stories did you end with, and why that number?** 6. Because 1 story is strange and i dont put it on

---

## 4. Original AI output — acceptance criteria (Part 3)

```
Assumptions:

Overlapping bookings ending/starting at the exact same hour are allowed.

Bookings lasting exactly two hours are permitted.

US-01: View availability
AC-1:
Given a student opens the availability screen,
When they select a room and date,
Then all free slots are displayed.

AC-2:
Given a room is booked from 10:00 to 12:00,
When a student checks availability for that room,
Then 10:00 to 12:00 shows as unavailable.

AC-3:
Given a room is blocked by an admin,
When a student checks its availability,
Then it shows as unavailable for all slots.

US-02: Book room
AC-4:
Given a room is available at 14:00,
When a student selects 14:00 to 16:00 and submits,
Then the reservation is confirmed.

AC-5:
Given a room is already booked at 14:00,
When another student tries to book 14:00 to 15:00,
Then an error message is displayed.

US-03: Cancel booking
AC-6:
Given a student has an upcoming booking,
When they click cancel,
Then the booking is removed and room becomes free.
```

---

## 5. Criteria review (Part 3)

| Criterion (as generated) | Problem | What I changed it to | Final ID |
| --- | --- | --- | --- |
| AC-1 | UI reference ("screen") and vague setup | Explicit state given, observable result without UI terms | AC-01 |
| AC-2 | Kept structure, clarified precondition | Explicitly defined active booking time range | AC-02 |
| AC-3 | Vague admin reference | Specific blocked status condition | AC-03 |
| AC-4 | Missing explicit current time check (R1) | Added current time precondition to verify future start | AC-04 |
| AC-5 | Lacked coverage for max duration rule (R2) | Added separate AC-07 for R2 duration test | AC-05 |
| AC-6 | UI reference ("click cancel"), missing error cases | Replaced with domain event, added past booking test | AC-09, AC-10 |

**The two open questions.** Write your decision and the reason. Either answer is accepted.

| Question | My decision | Why |
| --- | --- | --- |
| A booking ending exactly when another begins — overlap under R3? | allowed | Time slots touching at boundary points (e.g. 10:00-12:00 and 12:00-14:00) share zero duration and allow maximum utilization. |
| Is exactly two hours allowed under R2? | allowed | "At most two hours" is inclusive of the upper boundary value. |

**Which invalid or boundary case did the assistant leave out?**
The AI left out explicit negative validation cases for booking start times in the past (rule R1) and booking durations exceeding two hours (rule R2). Both were added during review as AC-06 and AC-07.

---

## 6. Original AI output — use-case diagram (Part 4)

```
@startuml
left to right direction

actor Student
actor Administrator
actor System

rectangle "Smart Campus study room booking" {
  usecase "View availability" as UC1
  usecase "Book room" as UC2
  usecase "Cancel booking" as UC3
  usecase "Block or unblock room" as UC4
  usecase "Review usage" as UC5
  usecase "Send confirmation" as UC6
}

Student --> UC1
Student --> UC2
Student --> UC3
Administrator --> UC4
Administrator --> UC5
System --> UC6
@endluml
```

Rendered diagram (image, or a link): image.png

---

## 7. Diagram review (Part 4)

| Element | Problem | What I changed |
| --- | --- | --- |
| Actor System | Introduced a third non-human actor outside boundary | Removed System actor completely. |
| Association System --> UC6 | External actor triggering system confirmation | Replaced with <<include>> relationships from UC02 and UC03 to UC06. |
| UC IDs | Used non-standard UC1-UC6 naming | Renamed use cases to UC01-UC06 matching assignment standard. |



**Associations.** Which actor–use-case links did the assistant draw that a person does not actually trigger? Name them.
The assistant drew an association between a "System" actor and UC-06 Send confirmation. Confirmation is an automated background task triggered by booking or cancellation actions, not an external actor.

**Did any screen, database or internal component appear as a use case or an actor?** Yes, the AI included "System" as an external actor. No screens or databases appeared inside the boundary.


---

## 8. Traceability (Part 5)

Summarise what the table in `requirements/traceability.md` shows:

- Use cases with no story behind them: None (all 6 use cases have corresponding stories US-01 through US-07).
- Stories with no use case they belong to: None.
- Criteria that test no rule from section 1: None (all criteria directly map to business rules R1–R4 or core functional paths).

**What does the largest gap tell you about the generated requirements?**
The initial AI generation skipped explicit business rule edge-case criteria (R1 past booking and R2 max duration), demonstrating that raw AI outputs default to superficial happy-path scenarios unless rigorously audited against business constraints.

---

## 9. Checker runs

Paste the **real terminal output** of both runs. A table with nothing behind it does not count.

```
$ python tests/check_requirements.py
PASS   US-1  user-stories.md         no placeholders left
PASS   US-2  user-stories.md         7 stories, IDs US-01…US-07
PASS   US-3  user-stories.md         every story has the required sentence shape
PASS   US-4  user-stories.md         every story has a priority
PASS   US-5  user-stories.md         every story declares an assumption
PASS   US-6  user-stories.md         only Student and Administrator appear as roles
PASS   US-7  user-stories.md         nothing from the out-of-scope list appears
PASS   AC-1  acceptance-criteria.md  no placeholders left
PASS   AC-2  acceptance-criteria.md  three sections, all naming real stories: US-01, US-02, US-03
PASS   AC-3  acceptance-criteria.md  every section has 3 to 5 uniquely numbered criteria
PASS   AC-4  acceptance-criteria.md  all 11 criteria are complete Given/When/Then
PASS   AC-5  acceptance-criteria.md  every section covers an invalid or boundary case
PASS   AC-6  acceptance-criteria.md  3 assumptions listed before the criteria
PASS   AC-7  acceptance-criteria.md  both open questions are settled in the assumptions
PASS   PU-1  use-cases.puml          valid PlantUML block, no placeholders
PASS   PU-2  use-cases.puml          exactly two actors: Student, Administrator
PASS   PU-3  use-cases.puml          all six use cases present
PASS   PU-4  use-cases.puml          system boundary present
PASS   PU-5  use-cases.puml          no screens, databases or internal components
PASS   PU-6  use-cases.puml          no unjustified actor associations found
PASS   TR-1  traceability.md         all six use cases have a row
PASS   TR-2  traceability.md         every ID in the table resolves
PASS   TR-3  traceability.md         every story appears in the table
------------------------------------------------------------------------
23 PASS · 0 FAIL · 0 ERROR   (23 checks)
Shape is clean. This says nothing about whether the requirements are good.
```

```
$ python tests/validate_submission.py
submission.yml — submission.yml         
------------------------------------------------------------------------
PASS   schema                                    1
PASS   week                                      03
PASS   student.name                              Мальцев Ярослав
PASS   student.student_id                        25B030214
PASS   student.github                            UnityFan228337
PASS   assistant.tool                            Gemini
PASS   assistant.model                           Gemini 3.6 Flash
PASS   counts.user_stories                       7
PASS   counts.acceptance_criteria_sets           3
PASS   checker                                   21 PASS · 2 FAIL · 0 ERROR
PASS   checker.commit                            91ac7b4
PASS   assumptions.overlap_touching_bookings     allowed
PASS   assumptions.exactly_two_hours             allowed
PASS   traceability.use_cases_not_covered        []
PASS   traceability.stories_not_traced           []
NOTE   traceability                              you are claiming full coverage in both directions — that is rare on a first pass, and it is checked
PASS   review_findings                           3 findings
PASS   review_findings[1]                        US-07 was added during story review because UC-06 Send confi…
PASS   review_findings[2]                        The AI originally connected Administrator directly to UC-06 …
PASS   review_findings[3]                        AC-06 and AC-07 were explicitly expanded to cover mandatory …
PASS   honesty.can_explain_everything_submitted  yes
PASS   honesty.ai_usage_disclosed                yes
------------------------------------------------------------------------
21 PASS · 0 FAIL · 0 ERROR · 1 note
Shape is fine. This says nothing about whether the work is good.
```

| | PASS | FAIL | ERROR |
| --- | --- | --- | --- |
| `check_requirements.py` | | | |

Commit these numbers were produced at (`git rev-parse --short HEAD`):

**Every FAIL, one line each: what it is and what you decided to do about it.** A FAIL you report and
explain costs you nothing.

**Did you run the checks by hand instead of with Python?** No 
<!-- Say so here — it costs nothing, but it
has to be said. -->

---

## 10. Conclusion (150–200 words)

Answer all three:

1. Which part of the generated requirements was most wrong, and how would you have caught it without
   a checker?
2. What did the assistant get right that would have taken you noticeably longer by hand?
3. You are handing these requirements to someone who will implement them, and you will not be in the
   room. Which single one would you rewrite first, and why?

<!-- Be specific. "The AI was useful" is worth nothing; "UC-06 had no story behind it until I wrote
US-07, and the checker is what told me" is worth everything. -->

The most incorrect part of the generated requirements was the use-case diagram's inclusion of a "System" actor triggering UC-06 Send confirmation, alongside the initial user story where the AI assigned "System" as a stakeholder role. Without automated checkers, this error is easily identified by verifying actor definitions against domain rules: system components cannot act as human stakeholders or external actors triggering internal processes.

Conversely, the assistant excelled at rapidly generating structured initial user story templates and Given/When/Then acceptance criteria frameworks, saving substantial drafting time.

If handing these requirements to an engineer without further discussion, I would immediately rewrite US-02 and its acceptance criteria (AC-04 through AC-08). Booking logic carries the highest technical complexity due to strict constraints on future timestamps (R1), two-hour limits (R2), overlap checks (R3), and blocked state handling (R4). Precise, unambiguous specifications for these boundary rules are critical to prevent concurrency defects and invalid database records during implementation.