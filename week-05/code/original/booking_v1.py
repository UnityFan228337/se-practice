def can_book(start, end, now, blocked, existing):
    """Return True only if the booking request satisfies AC1-AC5.

    Times are integer minutes after midnight on one date. Intervals include
    the start and exclude the end, so (600, 660) and (660, 720) only touch.
    """
    # AC1: valid interval inside the day, and in the future
    if not (0 <= start < end <= 1440):
        return False
    if start <= now:
        return False

    # AC2: at most 120 minutes
    if end - start > 120:
        return False

    # AC3: the room must not be blocked
    if blocked:
        return False

    # AC4: no overlap with any existing booking (touching endpoints allowed)
    for booked_start, booked_end in existing:
        if start < booked_end and booked_start < end:
            return False

    # AC5: every rule holds; existing was only read, never modified
    return True
