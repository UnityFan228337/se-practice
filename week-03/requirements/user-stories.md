# User stories — Smart Campus study room booking

6 to 8 stories. Keep the shape exactly: ID, the As/I want/so that sentence, a priority, one
assumption. Roles are **Student** or **Administrator** only.

---

### US-01
**Story:** As a Student, I want to view room availability for specific time slots, so that I can find an open study space for my schedule.
**Priority:** High
**Assumption:** The availability view reflects current bookings in real time without showing personal student details.

### US-02
**Story:** As a Student, I want to book an available study room for a future time slot, so that I have a guaranteed place to study.
**Priority:** High
**Assumption:** Room bookings can only be requested up to 14 days in advance.

### US-03
**Story:** As a Student, I want to cancel my existing room booking, so that the room becomes available for other students if I no longer need it.
**Priority:** Medium
**Assumption:** Cancellations can be performed anytime up until the start of the scheduled booking slot.

### US-04
**Story:** As an Administrator, I want to block a study room from being booked, so that students cannot reserve it.
**Priority:** High
**Assumption:** Blocking a room immediately prevents any new bookings from being created for that room.

### US-05
**Story:** As an Administrator, I want to unblock a previously blocked room, so that it becomes available for student reservations again.
**Priority:** Medium
**Assumption:** Unblocking a room restores its availability according to its standard operational schedule.

### US-06
**Story:** As an Administrator, I want to review room usage metrics over selected time periods, so that I can understand peak hours and optimize library room allocation.
**Priority:** Low
**Assumption:** Usage statistics are aggregated from historical booking data without violating student privacy.

### US-07
**Story:** As a Student, I want to receive an automated notification confirming my booking or cancellation action, so that I have written proof of my reservation status.
**Priority:** High
**Assumption:** Confirmation messages are generated automatically by the system immediately after a booking or cancellation transaction succeeds.