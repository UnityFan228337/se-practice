# Smart Campus Room Availability Checker

A single-page Python (Streamlit) app that lets a student check whether a
selected campus room is available for a requested time window.

It only **checks availability** — it never creates, confirms, or modifies
any booking. There is no login, no database, no backend, and no external API.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Acceptance criteria

- **AC1** Integer minutes, `0 <= start < end <= 1440`, and `start` strictly after `now`.
- **AC2** Duration at most 120 minutes; exactly 120 is permitted.
- **AC3** Reject every request when the room is blocked.
- **AC4** Reject overlap with any existing booking; touching at an endpoint is NOT overlap.
- **AC5** An unambiguous Available / Unavailable result; never mutates existing bookings.
- **AC6** Understandable validation feedback; usable narrow/mobile layout.

## Contract

```python
can_book(start, end, now, blocked, existing) -> bool
```

Returns `True` only when AC1–AC4 all hold. Pure function, no side effects.

## Fictional data

Four sample rooms (one blocked) with in-memory bookings, defined in `app.py`.
