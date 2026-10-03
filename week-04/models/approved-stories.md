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
