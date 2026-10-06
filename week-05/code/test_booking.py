"""Tests for can_book. Every expected value comes from AC1-AC5, never from running the code.

Base input unless a test says otherwise: now=540, blocked=False, existing=[(600, 660)].
Each test is built so that exactly one rule decides the result.
"""
import unittest

from booking import can_book


class BookingTests(unittest.TestCase):
    # ---- the six cases from the task table ------------------------------------------------
    def test_touching_end_is_allowed(self):
        result = can_book(660, 720, 540, False, [(600, 660)])
        self.assertIs(result, True)

    def test_overlap_is_rejected(self):
        # AC4 only: 60 minutes, in the future, room free
        self.assertIs(can_book(630, 690, 540, False, [(600, 660)]), False)

    def test_blocked_room_is_rejected(self):
        # AC3 only: the same request as the touching case, but the room is blocked
        self.assertIs(can_book(660, 720, 540, True, [(600, 660)]), False)

    def test_exactly_two_hours_is_allowed(self):
        # AC2: 120 minutes is "at most 120"
        self.assertIs(can_book(720, 840, 540, False, [(600, 660)]), True)

    def test_over_two_hours_is_rejected(self):
        # AC2 only: 121 minutes, nothing else wrong
        self.assertIs(can_book(720, 841, 540, False, [(600, 660)]), False)

    def test_starting_now_is_rejected(self):
        # AC1 "start > now" only: ends at 570, before the booking at 600
        self.assertIs(can_book(540, 570, 540, False, [(600, 660)]), False)

    # ---- AC1: future start ----------------------------------------------------------------
    def test_one_minute_after_now_is_allowed(self):
        self.assertIs(can_book(541, 571, 540, False, [(600, 660)]), True)

    def test_start_in_the_past_is_rejected(self):
        # AC1 only: ends at 530, before the booking at 600
        self.assertIs(can_book(500, 530, 540, False, [(600, 660)]), False)

    def test_now_zero_start_zero_is_rejected(self):
        self.assertIs(can_book(0, 60, 0, False, []), False)

    def test_now_zero_start_one_is_allowed(self):
        self.assertIs(can_book(1, 61, 0, False, []), True)

    # ---- AC1: zero-length, reversed, day bounds -------------------------------------------
    def test_zero_length_is_rejected(self):
        # AC1 "start < end" only: 700 is in the future, free and not too long
        self.assertIs(can_book(700, 700, 540, False, [(600, 660)]), False)

    def test_reversed_times_are_rejected(self):
        # AC1 "start < end" only: end before start, no booking is touched
        self.assertIs(can_book(720, 700, 540, False, [(600, 660)]), False)

    def test_end_exactly_at_midnight_is_allowed(self):
        # AC1 "end <= 1440": 1440 itself is allowed
        self.assertIs(can_book(1380, 1440, 540, False, []), True)

    def test_end_after_midnight_is_rejected(self):
        # AC1 "end <= 1440" only: 61 minutes, in the future, no overlap
        self.assertIs(can_book(1380, 1441, 540, False, []), False)

    def test_negative_start_is_rejected(self):
        # AC1: start must be at least 0 (start > now already implies it, see report 9.3)
        self.assertIs(can_book(-30, 30, 0, False, []), False)

    def test_last_minute_of_the_day_is_allowed(self):
        # Part 4 edge case: AC1 allows start 1439 / end 1440 when now is 1438
        self.assertIs(can_book(1439, 1440, 1438, False, []), True)

    # ---- AC2: duration --------------------------------------------------------------------
    def test_one_minute_booking_is_allowed(self):
        self.assertIs(can_book(720, 721, 540, False, [(600, 660)]), True)

    # ---- AC3: blocked ---------------------------------------------------------------------
    def test_blocked_room_with_no_bookings_is_rejected(self):
        self.assertIs(can_book(660, 720, 540, True, []), False)

    # ---- AC4: the other overlap relationships ---------------------------------------------
    def test_overlap_over_the_start_is_rejected(self):
        self.assertIs(can_book(570, 630, 540, False, [(600, 660)]), False)

    def test_inside_existing_booking_is_rejected(self):
        self.assertIs(can_book(615, 645, 540, False, [(600, 660)]), False)

    def test_containing_existing_booking_is_rejected(self):
        self.assertIs(can_book(570, 690, 540, False, [(600, 660)]), False)

    def test_identical_to_existing_booking_is_rejected(self):
        self.assertIs(can_book(600, 660, 540, False, [(600, 660)]), False)

    def test_ending_at_existing_start_is_allowed(self):
        # touching on the other side
        self.assertIs(can_book(570, 600, 540, False, [(600, 660)]), True)

    # ---- AC4: empty and several bookings --------------------------------------------------
    def test_empty_existing_is_allowed(self):
        self.assertIs(can_book(600, 660, 540, False, []), True)

    def test_overlap_with_second_booking_is_rejected(self):
        self.assertIs(can_book(720, 780, 540, False, [(600, 660), (700, 760)]), False)

    def test_overlap_in_unsorted_list_is_rejected(self):
        self.assertIs(can_book(610, 650, 540, False, [(900, 960), (600, 660)]), False)

    def test_fits_exactly_between_two_bookings(self):
        self.assertIs(can_book(660, 720, 540, False, [(600, 660), (720, 780)]), True)

    def test_free_slot_among_three_bookings(self):
        existing = [(600, 660), (700, 760), (800, 860)]
        self.assertIs(can_book(760, 800, 540, False, existing), True)

    # ---- AC5: unchanged input -------------------------------------------------------------
    def test_existing_unchanged_after_accepted_request(self):
        existing = [(900, 960), (600, 660), (700, 760)]
        before = list(existing)
        self.assertIs(can_book(780, 840, 540, False, existing), True)
        self.assertEqual(existing, before)

    def test_existing_unchanged_after_rejected_request(self):
        existing = [(900, 960), (600, 660), (700, 760)]
        before = list(existing)
        self.assertIs(can_book(610, 650, 540, False, existing), False)
        self.assertEqual(existing, before)

    def test_existing_unchanged_when_blocked(self):
        existing = [(900, 960), (600, 660)]
        before = list(existing)
        self.assertIs(can_book(780, 840, 540, True, existing), False)
        self.assertEqual(existing, before)

    # ---- AC5: the result is a real Boolean ------------------------------------------------
    def test_result_is_a_boolean_in_every_branch(self):
        for result in (
            can_book(660, 720, 540, False, [(600, 660)]),   # accepted
            can_book(630, 690, 540, False, [(600, 660)]),   # overlap
            can_book(660, 720, 540, True, [(600, 660)]),    # blocked
            can_book(720, 841, 540, False, [(600, 660)]),   # too long
            can_book(720, 700, 540, False, [(600, 660)]),   # reversed
        ):
            self.assertIsInstance(result, bool)

    # ---- outside the contract: documents report 9.2 (not counted by the checker) ----------
    def test_non_integer_time_is_not_handled_but_still_returns_a_boolean(self):
        # The contract says times are integers. can_book does no type checking (report 9.2),
        # so 600.5 goes through the same arithmetic as an integer and still yields a Boolean.
        self.assertIsInstance(can_book(600.5, 660.5, 540, False, []), bool)


if __name__ == "__main__":
    unittest.main()
