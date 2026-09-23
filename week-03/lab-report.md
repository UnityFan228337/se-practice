# Lab report — Practice #03, Requirements Engineering with AI

Fill in every section. **Do not delete or renumber the headings** — the README points at them and a
missing heading reads as a missing section.

Name:
Student ID:
GitHub username:

---

## 1. Setup

| | |
| --- | --- |
| AI assistant (tool) | Gemini |
| Exact model name and version | Gemini 3.6 Flash |
| Date of the session | 23.09 |
| Diagram renderer used | |

One tool and one model for all three prompts. If you switched, say why here — it changes what your
findings mean.

---

## 2. Original AI output — user stories (Part 1)

Paste the **unedited** response to Prompt 1. Do not tidy it. If it is long, paste all of it anyway;
this is the baseline everything else is measured against.

```
---

## Stakeholder Goals

### Student Goals

* **Discover Availability:** Quickly find available study spaces tailored to specific criteria (capacity, equipment, noise level).
* **Self-Service Reservation:** Reserve and manage study room slots directly without manual staff intervention.
* **Reservation Reliability:** Guarantee access to a reserved space upon arrival and easily check in.

### Administrator Goals

* **Resource Optimization:** Maximize study room utilization and prevent ghost bookings (no-shows).
* **Access Control & Governance:** Set room usage policies, operating hours, and booking limits to ensure fair access across campus.
* **Operational Monitoring:** Track usage analytics and maintain control over room statuses (e.g., maintenance shutdowns).

---

## User Stories

### Student Stories

#### 1. Real-Time Room Search

* **User Story:** As a **Student**, I want **to search for available study rooms by time, capacity, and equipment (e.g., whiteboards, monitors)**, so that **I can quickly find a space that fits my group's study needs.**
* **Priority:** High
* **Assumption:** The campus room database maintains real-time sync of room attributes and availability status.

#### 2. Instant Reservation

* **User Story:** As a **Student**, I want **to reserve an available room slot directly through the app**, so that **I can secure a space ahead of time without needing staff approval.**
* **Priority:** High
* **Assumption:** Students log in using active university SSO credentials to validate their eligibility.

#### 3. Room Check-In

* **User Story:** As a **Student**, I want **to check into my reserved room using a QR code or mobile check-in upon arrival**, so that **my booking is confirmed and not released to other students.**
* **Priority:** Medium
* **Assumption:** Rooms have standard QR codes or smart sensors integrated with the mobile system.

#### 4. Booking Management & Cancellation

* **User Story:** As a **Student**, I want **to view and cancel my upcoming reservations from my dashboard**, so that **I can adjust my schedule and free up unused rooms for others.**
* **Priority:** Medium
* **Assumption:** Cancellations can be performed up to a designated threshold (e.g., 15 minutes prior to start time).

---

### Administrator Stories

#### 5. Room Policy & Quota Management

* **User Story:** As an **Administrator**, I want **to define max booking durations and daily limits per student**, so that **room usage is distributed fairly across the entire student body.**
* **Priority:** High
* **Assumption:** System rules apply automatically during the student booking workflow.

#### 6. Automatic No-Show Release

* **User Story:** As an **Administrator**, I want **the system to automatically cancel bookings if a student fails to check in within 15 minutes**, so that **unclaimed spaces are made available for drop-in use.**
* **Priority:** High
* **Assumption:** The system runs automated background checks against pending reservations.

#### 7. Utilization Analytics

* **User Story:** As an **Administrator**, I want **to view reporting dashboards on peak usage times and popular room types**, so that **I can optimize campus facilities and staffing schedules.**
* **Priority:** Low
* **Assumption:** Historical booking and check-in logs are stored securely in a central database.

---
```

---

## 3. Story review (Part 2)

One row per change you made. "Kept unchanged" is a valid row and needs a reason too.

| Story (as generated) | What I did | Why | Final ID |
| --- | --- | --- | --- |
| As a Student, I want to search for available study rooms by time, capacity, and equipment (e.g., whiteboards, monitors), so that I can quickly find a space that fits my group's study needs. | Kept unchanged | i think story was made good | UC-01 |
| As a Student, I want to reserve an available room slot directly through the app, so that I can secure a space ahead of time without needing staff approval. | Kept unchanged | i think story was made good | UC-02 |
| As a Student, I want to view and cancel my upcoming reservations from my dashboard, so that I can adjust my schedule and free up unused rooms for others. | Kept unchanged| it fits in requirements| UC-03 |
| As an Administrator, I want the system to automatically cancel bookings if a student fails to check in within 15 minutes, so that unclaimed spaces are made available for drop-in use. Also add an ability to block if room out of service, and unblock when it fix.| add block and unblock | it almost fit, but he forgot to add block and unblock | UC-04 |
| As an Administrator, I want to define max booking durations and daily limits per student, so that room usage is distributed fairly across the entire student body. Also put cameras or watcher, that will check is all fine or not. | Add camearas or watchers | i think ai forget to add check a conditions of the rooms | UC-05 |
| As a Student, I want to check into my reserved room using a QR code or mobile check-in upon arrival, so that my booking is confirmed and not released to other students. | Kept unchanged | it fully fit in requirements | UC-06 |
| As an Administrator, I want to view reporting dashboards on peak usage times and popular room types, so that I can optimize campus facilities and staffing schedules. | Kept unchanged | i think it additional and dont write in condiotions of the task | UC-07 |

**Did the assistant invent anything outside the scenario?** QR-code for rooms, database and dashboards to see peak usage and popular room types

**How many stories did you end with, and why that number?** 6. Because 1 story is strange and i dont put it on

---

## 4. Original AI output — acceptance criteria (Part 3)

```
---
# Acceptance criteria — three selected stories

Assumptions first, then the criteria. Each block names the story it belongs to. 3 to 5 criteria per
story, every one in Given / When / Then form, and every set covers a validation or error case — not
three happy paths.

---

## Assumptions

These must settle the two questions the scenario leaves open. Either answer is accepted; no answer
is not.

- **Overlap:** a booking that ends exactly when another begins is allowed under R3, because back-to-back bookings share an instantaneous boundary (half-open time interval `[start, end)`) rather than overlapping actual time slots.
- **Duration:** a booking of exactly two hours is allowed under R2, because the restriction specifies a maximum duration of two hours (inclusive of the 2-hour boundary).
- **Rule Constraints:** All booking attempts must be for future time slots relative to current system time, blocked rooms cannot be booked under any conditions, and max duration/daily limit rules are enforced at time of request.
- **Story 3 Scope:** Physical camera/watcher integration is treated as a monitoring feature; automated space usage status or policy breach alerts trigger standard system flags/notifications.

---

## Story 1 — Reporting Dashboards on Peak Usage & Room Types

### AC-01
- **Given** an Administrator is logged into the management portal with valid credentials
- **When** the Administrator navigates to the "Campus Analytics" section and selects a date range
- **Then** the system displays a dashboard showing peak room usage hours and the top requested room types with aggregate usage percentages.

### AC-02
- **Given** an Administrator is viewing the reporting dashboard
- **When** the Administrator applies filters for capacity, time frame, or building location
- **Then** the dashboard dynamically updates the graphs and summary tables to reflect data matching only the selected filter criteria.

### AC-03
- **Given** an Administrator attempts to generate a report for a date range where no room booking or usage data exists
- **When** the custom date filter is applied
- **Then** the system displays an informational message "No booking data available for the selected period" and shows empty graph states without crashing or failing silently.

---

## Story 2 — Student Search for Available Study Rooms

### AC-04
- **Given** a Student searches for a study room for a future time slot of 1.5 hours with capacity for 4 people and a whiteboard requirement
- **When** the search request is submitted
- **Then** the system returns a list of available, unblocked rooms matching or exceeding all requested criteria that have no overlapping bookings during that interval.

### AC-05
- **Given** a Student searches for a study room selecting a duration of 3 hours or a time slot in the past
- **When** the Student executes the search query
- **Then** the system prevents submission and displays a validation error message stating "Bookings must be scheduled for future times and cannot exceed the maximum duration of 2 hours."

### AC-06
- **Given** Room 101 is marked as "Blocked" (e.g., undergoing maintenance) for the entire afternoon
- **When** a Student searches for an available room with matching capacity and equipment during that afternoon interval
- **Then** Room 101 is excluded from the search results, ensuring blocked or overlapping rooms cannot be booked.

---

## Story 3 — Administrator Booking Limits & Presence Watcher

### AC-07
- **Given** an Administrator configures the daily student booking limit to 1 active reservation per day with a max duration of 2 hours
- **When** a Student submits a valid reservation request for 2 hours in the future
- **Then** the system successfully creates the booking and logs the reservation against the student's daily threshold.

### AC-08
- **Given** a Student already has a 2-hour booking for today or attempts to create a single booking exceeding 2 hours
- **When** the Student attempts to finalize a new booking for the same day
- **Then** the system rejects the request, displays an error message stating "Booking limit reached or maximum duration exceeded," and leaves room availability unchanged.

### AC-09
- **Given** an automated camera/watcher device is active in an occupied or reserved study room
- **When** the watcher detects non-compliance (e.g., an unbooked/blocked room is occupied, or no occupancy detected 15 minutes after start time)
- **Then** the system logs an event alert on the Administrator dashboard indicating a potential facility rule breach or no-show status.
```

---

## 5. Criteria review (Part 3)

| Criterion (as generated) | Problem | What I changed it to | Final ID |
| --- | --- | --- | --- |
| | | | |

**The two open questions.** Write your decision and the reason. Either answer is accepted.

| Question | My decision | Why |
| --- | --- | --- |
| A booking ending exactly when another begins — overlap under R3? | allowed / not-allowed | |
| Is exactly two hours allowed under R2? | allowed / not-allowed | |

**Which invalid or boundary case did the assistant leave out?**

---

## 6. Original AI output — use-case diagram (Part 4)

```
(paste the PlantUML source exactly as generated)
```

Rendered diagram (image, or a link):

---

## 7. Diagram review (Part 4)

| Element | Problem | What I changed |
| --- | --- | --- |
| | | |

**Associations.** Which actor–use-case links did the assistant draw that a person does not actually
trigger? Name them.

**Did any screen, database or internal component appear as a use case or an actor?**

---

## 8. Traceability (Part 5)

Summarise what the table in `requirements/traceability.md` shows:

- Use cases with **no story** behind them:
- Stories with **no use case** they belong to:
- Criteria that test **no rule** from section 1:

**What does the largest gap tell you about the generated requirements?**

---

## 9. Checker runs

Paste the **real terminal output** of both runs. A table with nothing behind it does not count.

```
$ python tests/check_requirements.py
(paste)
```

```
$ python tests/validate_submission.py
(paste)
```

| | PASS | FAIL | ERROR |
| --- | --- | --- | --- |
| `check_requirements.py` | | | |

Commit these numbers were produced at (`git rev-parse --short HEAD`):

**Every FAIL, one line each: what it is and what you decided to do about it.** A FAIL you report and
explain costs you nothing.

**Did you run the checks by hand instead of with Python?** Say so here — it costs nothing, but it
has to be said.

---

## 10. Conclusion (150–200 words)

Answer all three:

1. Which part of the generated requirements was most wrong, and how would you have caught it without
   a checker?
2. What did the assistant get right that would have taken you noticeably longer by hand?
3. You are handing these requirements to someone who will implement them, and you will not be in the
   room. Which single one would you rewrite first, and why?

Be specific. "The AI was useful" is worth nothing; "UC-06 had no story behind it until I wrote
US-07, and the checker is what told me" is worth everything.
