# Week 04 — Lab report: Modeling the System with UML

> The single worksheet for this lab. Fill in every section. **Do not delete, rename or renumber
> the headings** — the checker and the grader find your work by them. Replace every `<...>`
> placeholder; a row that still contains `<...>` counts as empty.

---

## 1. Setup

| Field | Value |
| --- | --- |
| Name | Мальцев Ярослав |
| Group | [CSCI-2208] Software Engineering - Fall 2026 |
| AI assistant | Gemini |
| Exact model | Gemini 3.6 Flash |
| Renderer | PlantUML web server |
| Behaviour diagram | both |
| Stories used | my week-03 stories |

---

## 2. Prompts as sent

Paste every prompt **exactly as you sent it**, in the order you sent it, one code block each. The
AI's first replies are saved as files in `models/original/` — do not paste them here.

### 2.1 Task 1 — use-case prompt

```text
Using the supplied scenario and approved stories, generate PlantUML for a use-case diagram. Include Student and
Administrator outside a named system boundary. Model their goals, show justified associations, and list assumptions.
Use include or extend only with a clear reason. 
```

### 2.2 Task 2 — class prompt

```text
Create a UML domain class diagram in PlantUML for Smart Campus. Start with Student, Room, and Booking. Add
attributes, appropriate operations, and association multiplicities. Add other classes only when requirements justify
them. Explain each relationship and list assumptions. Avoid unjustified inheritance or composition. 
```

### 2.3 Task 3 — behaviour prompt (3A sequence or 3B activity)

```text
Generate PlantUML for Book room. Use Student, BookingService, and BookingRepository lifelines. Validate the supplied
rules, then attempt the reservation. Show a successful confirmation and an unavailable-room alternative using alt.
Label messages and replies. Explain new design components and all assumptions. 
```

<!-- didnt sent
### 2.4 Focused correction prompts (if you sent any)

```text
<paste, or write "none">
``` -->

### 2.5 Critique prompt

```text
# Approved stories — Smart Campus study room booking

> **Replace this file's stories with your own Week 03 stories, as revised after review**
> (`week-03/requirements/user-stories.md`), keeping their IDs. If you did not complete Week 03, or
> your set was rejected in review, keep the reference set below and say so in `lab-report.md` §1.
> Either way, the IDs here are the ones your consistency table (§7) must use.

**Source of this set:** week-03 stories, revised

## Scenario (from the Lesson 04 practice deck, slide 7)

Students view room availability, book a room, and cancel their own bookings. Administrators block
or unblock rooms and review usage.

- **R1** Future start, with duration greater than 0 and at most 2 hours.
- **R2** Active bookings for the same room cannot overlap.
- **R3** A blocked room cannot accept a new booking.
- **R4** A successful booking produces a confirmation.

## Reference set

| ID | Story | Rules |
| --- | --- | --- |
| US-01 | As a Student, I want to view room availability for specific time slots, so that I can find an open study space for my schedule. | R1, R2, R3, R4 |
| US-02 | As a Student, I want to book an available study room for a future time slot, so that I have a guaranteed place to study. | R1, R2, R3, R4 |
| US-03 | As a Student, I want to cancel my existing room booking, so that the room becomes available for other students if I no longer need it. | R1, R2, R3, R4 |
| US-04 | As an Administrator, I want to block a study room from being booked, so that students cannot reserve it. | R1, R2, R3, R4 |
| US-05 | As an Administrator, I want to unblock a previously blocked room, so that it becomes available for student reservations again. | R1, R2, R3, R4 |
| US-06 | As an Administrator, I want to review room usage metrics over selected time periods, so that I can understand peak hours and optimize library room allocation. | R1, R2, R3, R4 |

**Out of scope** (do not model): payments, equipment in rooms, recurring bookings, waiting lists,
notifications other than the booking confirmation, user registration.


@startuml
left to right direction
skinparam packageStyle rectangle

actor "Student" as student
actor "Administrator" as admin

rectangle "Smart Campus System" {
  
  package "Room Availability & Booking" {
    usecase "View Room Availability" as UC_View
    usecase "Book Study Room" as UC_Book
    usecase "Cancel Room Booking" as UC_Cancel
  }

  package "Room Management" {
    usecase "Block Study Room" as UC_Block
    usecase "Unblock Study Room" as UC_Unblock
    usecase "Review Room Usage Metrics" as UC_Metrics
  }

  package "Notifications" {
    usecase "Send Automated Confirmation" as UC_Notify
  }

}

' Student Associations
student -- UC_View
student -- UC_Book
student -- UC_Cancel

' Administrator Associations
admin -- UC_Block
admin -- UC_Unblock
admin -- UC_Metrics

' Include Relationships (Mandatory System Behaviors)
UC_Book ..> UC_Notify : <<include>>
UC_Cancel ..> UC_Notify : <<include>>

@enduml

@startuml
skinparam classAttributeIconSize 0
hide empty members

class Student {
  - studentId: String
  - name: String
  - email: String
  + viewAvailability(timeSlot: TimeSlot): List<RoomAvailability>
  + bookRoom(roomId: String, slot: TimeSlot): Booking
  + cancelBooking(bookingId: String): boolean
}

class Administrator {
  - adminId: String
  - name: String
  + blockRoom(roomId: String): boolean
  + unblockRoom(roomId: String): boolean
  + reviewUsageMetrics(period: TimeSlot): UsageMetrics
}

class Room {
  - roomId: String
  - roomNumber: String
  - capacity: int
  - isBlocked: boolean
  + isAvailable(slot: TimeSlot): boolean
  + setBlockedStatus(blocked: boolean): void
}

class Booking {
  - bookingId: String
  - timeSlot: TimeSlot
  - status: BookingStatus
  - createdAt: DateTime
  + isValidDuration(): boolean
  + cancel(): void
}

class TimeSlot {
  - startTime: DateTime
  - endTime: DateTime
  + getDurationInMinutes(): int
  + getDurationInHours(): string
  + overlapsWith(other: TimeSlot): boolean
  + isWithinDaysInAdvance(days: int): boolean
  + isFuture(): boolean
}

class ConfirmationNotification {
  - notificationId: String
  - recipientEmail: String
  - messageText: String
  - sentAt: DateTime
  - type: NotificationType
  + send(): void
}

enum BookingStatus {
  CONFIRMED
  CANCELLED
}

enum NotificationType {
  BOOKING_CONFIRMATION
  CANCELLATION_CONFIRMATION
}

' Relationships & Multiplicities
Student "1" -- "0..*" Booking : creates / owns >
Room "1" -- "0..*" Booking : reserved under >
Booking "1" *-- "1" TimeSlot : scheduled for >
Booking "1" -- "1..*" ConfirmationNotification : triggers >
Administrator "0..*" -- "0..*" Room : manages >

@enduml

@startuml
autonumber
actor "s:Student" as Student
participant ":BookingService" as Service
participant ":BookingRepository" as Repo
participant ":NotificationService" as Notify

Student -> Service : bookRoom(studentId, roomId, slot)
activate Service

' Step 1: Rule Validation
note over Service
**Validation Checks:**
- **R1:** Duration > 0 and <= 2 hours & in future
- **US-02:** Slot <= 14 days in advance
end note

alt Invalid TimeSlot (R1 / US-02 violation)
Service --> Student : return BookingError("Invalid duration or slot beyond 14 days")
else Valid TimeSlot
' Step 2: Check Availability & Room Status (R2 & R3)
Service -> Repo : isRoomAvailable(roomId, slot)
activate Repo
Repo --> Service : status (Available / Overlapped / Blocked)
deactivate Repo

alt Room Available (R2 & R3 Passed)
' Successful Reservation Path
Service -> Repo : saveBooking(booking)
activate Repo
Repo --> Service : confirmationRef
deactivate Repo

' Rule R4: Automated Confirmation
Service -> Notify : sendBookingConfirmation(studentId, confirmationRef)
activate Notify
Notify --> Service : notificationSent
deactivate Notify

Service --> Student : return BookingConfirmation(status=CONFIRMED, ref)

else Room Unavailable or Blocked (R2 / R3 Violation)
' Alternative Path: Room is Overlapped (R2) or Blocked (R3)
Service --> Student : return BookingError("Room unavailable or currently blocked")
end
end

deactivate Service
@enduml

Compare my diagrams with the requirements. Identify missing rules, inconsistent names, and unjustified elements.
Cite each issue and propose a specific correction. 
```

---

## 3. Task 1 — use-case review

**Assumptions the AI listed:** <one line each, or "the AI listed none" — that is a finding too>

At least **two** findings. A finding names the element, the problem and the rule or story that
proves it is a problem.

| # | Element | Problem | Rule or story | Fix |
| --- | --- | --- | --- | --- |
| 1 | Cancel Room Booking → Send Automated Confirmation (include) | A cancellation is made to produce a confirmation. R4 only gives a confirmation to a successful booking, and "notifications other than the booking confirmation" are out of scope. | R4, US-03, out-of-scope list in approved-stories.md | Proposed: delete the include from Cancel Room Booking (not yet applied in `models/use-case.puml`). |
| 2 | Send Automated Confirmation (use case) | A confirmation is a system outcome of booking, not a goal a student or administrator sets out to achieve. No actor is linked to it (UC5 passes), but it stays a use case of its own. | R4, US-01 ("I get a confirmation when the booking succeeds") | Proposed: keep it only as an include of Book Study Room, with the reason written down; or fold it into Book Study Room (not yet applied). |
| 3 | Both include arrows (lines 41 and 42) | No `' why:` comment directly above, which the §4 conventions require for every include. This is checker UC8. | README §4 convention, R4 | Proposed: add `' why: R4 - every successful booking produces a confirmation` above the remaining include (not yet applied). |
---

## 4. Task 2 — class diagram review

### 4.1 Relationships, read both ways

One row per association in your **revised** class diagram.

| Association | Read left → right | Read right → left | Multiplicities |
| --- | --- | --- | --- |
| Student — Booking | One student creates 0..* bookings. | Each booking belongs to exactly 1 student. | 1 / 0..* |
| Room — Booking | One room is reserved under 0..* bookings. | Each booking is for exactly 1 room. | 1 / 0..* |
| Booking — TimeSlot (composition) | Each booking is scheduled for exactly 1 time slot. | Each time slot belongs to exactly 1 booking. | 1 / 1 |
| Booking — ConfirmationNotification | One booking triggers 1 or more confirmations. | Each confirmation belongs to exactly 1 booking. | 1 / 1..* |
| Administrator — Room | One administrator manages 0..* rooms. | One room is managed by 0..* administrators. | 0..* / 0..* |

### 4.2 Constraints the multiplicities cannot show

- R2: the revised diagram does **not** state it. There is no note on `Booking`; the only trace is the operation `TimeSlot.overlapsWith(other)`. Checker CL8 fails for this reason. Proposed: a note on `Booking` saying that active bookings of the same room must not overlap.
- R1: at most 2 hours and a future start are visible only as operations (`Booking.isValidDuration()`, `TimeSlot.getDurationInMinutes()`, `TimeSlot.isFuture()`), not as a stated limit.
- R3: carried by the attribute `Room.isBlocked`; "a blocked room cannot accept a new booking" is not written anywhere on the diagram.

### 4.3 Assumptions

- A1: touching bookings do not overlap. A booking ending at 12:00 and another starting at 12:00 in the same room are both allowed (`allowed` in submission.yml).
- A2: blocking a room does not touch existing bookings. R3 and US-04 only stop new bookings, so existing ones are kept (`keep-bookings` in submission.yml).
- A3: a successful booking has exactly one confirmation, and a cancelled booking has none.
- A4: duration is measured in whole minutes, so "exactly 2 hours" (120 minutes) is allowed under R1.

### 4.4 Findings

| # | Element | Problem | Rule or story | Fix |
| --- | --- | --- | --- | --- |
| 1 | Booking "1" -- "1..*" ConfirmationNotification | 1..* says a booking can have many confirmations and must have at least one, which is wrong for a cancelled booking. | R4, A3 | Proposed: 0..1 on the confirmation end (not yet applied). |
| 2 | enum NotificationType (CANCELLATION_CONFIRMATION) and the `type` attribute | A cancellation confirmation is out of scope, and with one kind of confirmation the enum has nothing to distinguish. | Out-of-scope list, R4 | Proposed: remove the enum and the attribute (not yet applied). |
| 3 | Administrator "0..*" -- "0..*" Room : manages | No rule or story says which administrator manages which room; the association invents a relationship. Blocking is a state of the room (`Room.isBlocked`). | R3, US-04, US-05 | Proposed: remove the association, or justify an Administrator class by a requirement (not yet applied). |
| 4 | Booking (note) | R2 is stated nowhere on the diagram (checker CL8). | R2 | Proposed: add a note on Booking (not yet applied). |
| 5 | Booking *-- TimeSlot | Composition without the required `' why:` comment (checker CL5). It is defensible, because a time slot is a value that exists only as part of one booking, but the reason is not written. | README §4 convention | Proposed: add `' why: a time slot exists only as the start/end of one booking` above the line (not yet applied). |

---

## 5. Task 3 — behaviour diagram review

**Option chosen and why:** 3A sequence — it shows the order of the checks and which component performs each, which is where an assistant most often saves a booking before validating it.
 
**Design components added beyond the domain model:** `BookingService` — receives the booking request, validates R1 and coordinates the steps; `BookingRepository` — looks up room availability and saves the booking; `NotificationService` — sends the booking confirmation required by R4 (the AI added this lifeline; it was not in the prompt, which asked for three lifelines).
 
| # | Element | Problem | Rule or story | Fix |
| --- | --- | --- | --- | --- |
| 1 | Note "US-02: Slot ≤ 14 days in advance" and the first alt branch | The 14-day limit is attributed to US-02, but US-02 is "see which rooms are free" and no rule limits the advance. The AI invented a requirement and cited a story that does not say it. | R1, US-02 | Proposed: remove the 14-day condition from the note and the guard (not yet applied). |
| 2 | alt "Room Available (R2 and R3 Passed)" with the reply "status (Available / Overlapped / Blocked)" | R2 and R3 are collapsed into one decision, so the student gets one message for two different reasons. The business rules also sit inside `BookingRepository`, which should only store and fetch. | R2, R3 | Proposed: ask the repository for facts and let `BookingService` decide R3 and then R2 in two separate guarded branches (not yet applied). |
| 3 | Message saveBooking(booking) | No message creates the Booking, so the object appears from nowhere. Validation does come before saving, which is correct (SQ3, SQ4 pass). | R1, R4 | Proposed: add a create-booking message after the checks pass (not yet applied). |
| 4 | NotificationService lifeline | It is neither a domain class nor one of the three requested lifelines. It is justified by R4, so it is kept and explained above. | R4 | None: explained in this section. |

---

## 6. AI critique

Run the critique prompt once, on all your revised diagrams together. At least **three** rows. A
critique is another claim to evaluate, not a verdict: reject what is wrong and say why.

 # | Issue the AI raised | Element it cited | Verdict | Why |
| --- | --- | --- | --- | --- |
| 1 | R2 is not stated anywhere in the class diagram. | Booking (no note) | accept | Confirmed by checker CL8; multiplicities cannot show "no overlap", so a note on Booking is required. |
| 2 | Cancel Room Booking includes Send Automated Confirmation, but R4 covers only successful bookings. | Cancel Room Booking → Send Automated Confirmation | accept | R4 and the out-of-scope list give a confirmation only to a booking, not to a cancellation. |
| 3 | Booking has no start attribute, so R1's future start cannot be stated. | Booking.timeSlot (checker CL7) | reject | The start is `TimeSlot.startTime`, reached through the composition, and `TimeSlot.isFuture()` checks it. The data is there; only the checker looks for it on Booking itself. |
| 4 | Booking to ConfirmationNotification uses 1..*, which contradicts "a booking produces a confirmation". | Booking "1" -- "1..*" ConfirmationNotification | accept | One confirmation per successful booking, none per cancelled one (A3). |
| 5 | NotificationService is an unrequested lifeline that should be removed. | NotificationService (sequence) | reject | R4 requires a confirmation and something has to send it. It stays and is named as a design component in §5. |
| 6 | The Administrator — Room association and the Administrator class have no source in the rules. | Administrator "0..*" -- "0..*" Room | accept | None of R1–R4 or US-01 to US-06 names who manages which room; the association is invented. |

---

## 7. Consistency table

One row for each of **R1–R4**, then one row for **every use case in your revised use-case
diagram**, spelled exactly as in the diagram, with the story ID it traces to.

| Requirement / story | Use case | Classes | Behaviour element |
| --- | --- | --- | --- |
| R1 | Book Study Room | TimeSlot (startTime, endTime, isFuture), Booking.isValidDuration | Note "R1: duration above 0 and at most 2 hours, in the future" and the first alt branch |
| R2 | Book Study Room | Booking (timeSlot, status), TimeSlot.overlapsWith; the R2 note is missing | Repository reply "Overlapped" inside the second alt |
| R3 | Block Study Room | Room (isBlocked), Room.setBlockedStatus | Repository reply "Blocked" inside the second alt |
| R4 | Send Automated Confirmation | Booking, ConfirmationNotification | Message sendBookingConfirmation to NotificationService |
| US-01 | Book Study Room | Student, Room, Booking, TimeSlot | Whole sequence: bookRoom, checks, saveBooking, confirmation reply |
| US-01 | Send Automated Confirmation | Booking, ConfirmationNotification | Message sendBookingConfirmation and the reply BookingConfirmation |
| US-02 | View Room Availability | Student.viewAvailability, Room.isAvailable | not shown in the Book room sequence |
| US-03 | Cancel Room Booking | Booking (status CANCELLED), Booking.cancel | not shown in the Book room sequence |
| US-04 | Block Study Room | Administrator.blockRoom, Room (isBlocked) | not shown in the Book room sequence |
| US-05 | Unblock Study Room | Administrator.unblockRoom, Room (isBlocked) | not shown in the Book room sequence |
| US-06 | Review Room Usage Metrics | Administrator.reviewUsageMetrics | not shown in the Book room sequence |

---

## 8. Change log

At least **three** rows, and at least one for each required diagram (use case, class, your
behaviour diagram). "Before" is what the AI produced; "After" is what you submitted.

| # | Diagram | Before (AI's original) | After (your revision) | Reason |
| --- | --- | --- | --- | --- |
| 1 | use case | 7 use cases; Book and Cancel each include Send Automated Confirmation, no `' why:` comments | Same elements and includes; only a remark line was added above `@startuml` | No element was changed; the findings in §3 are open and not yet applied |
| 2 | class | TimeSlot.getDurationInHours(): double | getDurationInMinutes(): int added; getDurationInHours() now returns string | Author's choice: minutes as the integer base, hours derived from it for display |
| 3 | sequence | Original sequence with 4 lifelines and the 14-day note | Same sequence; only a remark line was added after `@enduml` | No element was changed; the findings in §5 are open and not yet applied |

---

## 9. Checker output

Paste the complete output of `python tests/check_models.py`, then explain **every FAIL you are
keeping**. The same IDs go in `submission.yml` under `checker.kept_fails`. A FAIL you report and explain costs you nothing. One you hide costs the whole criterion.

```text
Week 04 structural check - shape only, never quality
 
UC1  PASS  Student and Administrator declared
UC2  PASS  named system boundary: "Smart Campus System"
UC3  PASS  all actors declared outside the boundary
UC4  PASS  all scenario goals present (7 use cases)
UC5  PASS  no actor is associated with a confirmation use case
UC6  PASS  actor responsibilities match the scenario
UC7  PASS  use cases are goals, not screens or components
UC8  FAIL  no ' why: comment directly above: line 41 (include), line 42 (include)
UC9  PASS  revised diagram differs from the AI's original
CL1  PASS  Student, Room and Booking present
CL2  PASS  Booking is associated with Student and with Room
CL3  PASS  every association has multiplicities at both ends
CL4  PASS  1 student / 1 room per booking, 0..* bookings per student and per room
CL5  FAIL  no ' why: comment directly above: Booking-TimeSlot (composition)
CL6  PASS  only domain concepts in the class diagram
CL7  FAIL  Booking has no start attribute (R1)
CL8  FAIL  no note states R2 - multiplicity cannot show 'no overlap'; add a note on Booking
SQ1  PASS  Student, BookingService and BookingRepository lifelines present
SQ2  PASS  alt block with a guard on every branch (4 branches)
SQ3  PASS  validation happens before creation
SQ4  PASS  nothing is saved on a failure branch
SQ5  PASS  every message is labelled
SQ6  PASS  R1 (time range) is visible - checked or stated as a precondition
SQ7  PASS  R3 (blocked room) is visible
FI1  PASS  the AI's original output is kept for every diagram
FI2  PASS  a rendered image for every diagram
LR1  PASS  §1 setup filled (tool and model recorded)
LR2  FAIL  §2 needs the task 1, 2, 3 and critique prompts pasted (found 3)
LR3  PASS  3 use-case findings in §3
LR4  PASS  §4 relationships read both ways, 4 assumption(s) declared
LR5  PASS  4 behaviour-diagram findings in §5
LR6  PASS  5 critique issues with a verdict
LR7  FAIL  §8 needs >= 3 rows and one per diagram (rows: 0, missing: use case, class, behaviour)
CS1  PASS  6 approved stories
CS2  FAIL  §7 has no filled row for: R1, R2, R3, R4
CS3  FAIL  use case(s) with no §7 row tracing to an approved story: Block Study Room, Book Study Room, Cancel Room Booking, Review Room Usage Metrics, Send Automated Confirmation, Unblock Study Room, View Room Availability
CS4  PASS  every lifeline is a domain class or an explained design component
 
SUMMARY pass=29 fail=8 error=0
A FAIL you report and explain in lab-report.md §9 costs you nothing. One you hide costs the criterion.
```
 
**FAILs I am keeping, and why:**
 
- UC8 — the two includes still have no `' why:` comment; open, see §3 finding 3.
- CL5 — Booking *-- TimeSlot has no `' why:` comment; the composition itself is defended in §4.4 finding 5.
- CL7 — kept: the start is `TimeSlot.startTime`, reached through the composition (see §6 row 3).
- CL8 — no R2 note on Booking; open, see §4.4 finding 4.
- LR2 — only 3 prompts are pasted in §2, the checker needs 4 (task 1, 2, 3 and critique); the missing one is still to be added.
- LR7 — this run was made before §8 was filled in (0 rows found); §8 now has 3 rows, one per diagram.
- CS2 — this run was made before §7 was filled in; §7 now has rows for R1–R4.
- CS3 — same cause: §7 now has a row for every use case, each tracing to a US-ID.


---

## 10. Conclusion (120–180 words)

<!-- <Which diagram did the AI get most wrong, and what exactly was wrong? Which error would have
reached the code if nobody had reviewed it? What did the critique find that you missed — and what
did it claim that was false? Be specific: "the AI got the multiplicities wrong" is worth nothing;
"the AI put 1..* on the Booking end, which says every room must already have a booking" is worth
everything.> -->


The AI got the class diagram most wrong. It put 1..* on the ConfirmationNotification end of Booking, which says every booking, even a cancelled one, must already have at least one confirmation, and it added a CANCELLATION_CONFIRMATION type for a notification the scenario puts out of scope. The error that would have reached the code is in the sequence diagram: the AI cited US-02 for a 14-day advance limit that no story contains, so a developer would have built a rule nobody asked for. It also merged R2 and R3 into one "Room Available" branch, so a rejected student cannot be told whether the room was blocked or taken. The critique found what I missed on the use-case diagram: Cancel includes a confirmation that R4 never gives a cancellation. It claimed Booking has no start attribute, which is false, because the start sits in TimeSlot.startTime. The §3 and §5 fixes are still open.