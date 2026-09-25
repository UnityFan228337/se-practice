# Acceptance criteria — three selected stories

Assumptions first, then the criteria. Each block names the story it belongs to. 3 to 5 criteria per
story, every one in Given / When / Then form, and every set covers a validation or error case — not
three happy paths.

---

## Assumptions

These must settle the two questions the scenario leaves open. Either answer is accepted; no answer
is not.

- **Overlap:** a booking that ends exactly when another begins is allowed under R3, because back-to-back bookings do not share common time intervals.
- **Duration:** a booking of exactly two hours is allowed under R2, because the rule specifies a maximum duration of at most two hours inclusive.
- Room availability and block status are evaluated instantaneously upon request submission.

---

## US-01 — View availability

### AC-01
- **Given** room 101 is unblocked and has no bookings between 14:00 and 16:00,
- **When** the Student requests the availability schedule for room 101 for today,
- **Then** the system displays room 101 as available for the 14:00–16:00 time slot.

### AC-02
- **Given** room 102 has an active booking from 10:00 to 12:00,
- **When** the Student views availability for room 102 for today,
- **Then** the time slot 10:00 to 12:00 is marked as occupied and cannot be selected.

### AC-03
- **Given** room 103 has been blocked by the Administrator,
- **When** the Student views room availability for room 103,
- **Then** room 103 is clearly indicated as blocked/unavailable for all time slots.

---

## US-02 — Book room

### AC-04
- **Given** room 104 is unblocked and free from 14:00 to 16:00, and the current time is 10:00,
- **When** the Student submits a booking request for room 104 from 14:00 to 16:00,
- **Then** the reservation is successfully confirmed.

### AC-05
- **Given** room 105 has an existing reservation from 14:00 to 15:30,
- **When** the Student attempts to book room 105 from 15:00 to 16:30,
- **Then** the system rejects the booking due to schedule overlap (R3 rule violation).

### AC-06
- **Given** the current time is 11:00,
- **When** the Student attempts to book a room from 10:00 to 12:00 (a past start time),
- **Then** the system rejects the request with an error stating that bookings must start in the future (R1 rule violation).

### AC-07
- **Given** room 106 is free starting at 13:00,
- **When** the Student attempts to create a reservation from 13:00 to 15:30 (duration of 2.5 hours),
- **Then** the system denies the request for exceeding the maximum allowed duration of two hours (R2 rule violation).

### AC-08
- **Given** room 107 is currently blocked by the Administrator,
- **When** the Student attempts to book room 107 for tomorrow from 10:00 to 12:00,
- **Then** the system rejects the booking request because the room is blocked (R4 rule violation).

---

## US-03 — Cancel booking

### AC-09
- **Given** the Student has an active future booking for room 108 starting at 15:00 today,
- **When** the Student cancels the booking at 13:00 today,
- **Then** the system cancels the reservation and marks room 108 as available for 15:00.

### AC-10
- **Given** a reservation for room 109 ended yesterday at 16:00,
- **When** the Student attempts to cancel the past reservation,
- **Then** the system prevents cancellation and retains the historical record.

### AC-11
- **Given** Student A has a valid reservation for room 110,
- **When** Student B attempts to submit a cancellation request for Student A's booking,
- **Then** the system denies the cancellation operation.