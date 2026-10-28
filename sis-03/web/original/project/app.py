#!/usr/bin/env python3
"""
Smart Campus Room Availability Checker — stdlib only (no third-party libs).

Runs an HTTP server on http://localhost:8000 that serves ONE responsive
page. Clicking "Check availability" calls /check, which evaluates the pure
contract can_book(start, end, now, blocked, existing) on the server.

Scope (per user story):
  - One responsive page, one selected room, fictional bookings.
  - CHECKS AVAILABILITY ONLY — never creates, confirms, or mutates bookings.
  - NO login, NO database, NO backend persistence, NO external APIs, NO payments.

Run:  python3 app.py
Then open http://localhost:8000 in a browser.
"""

from __future__ import annotations

import json
import urllib.parse
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import List, Tuple

PORT = 8000
MINUTES_PER_DAY = 1440
MAX_DURATION_MIN = 120


# ---------------------------------------------------------------------------
# Fictional data (in-memory only; never persisted, never mutated by the UI)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Booking:
    start: int  # minutes from midnight, inclusive
    end: int    # minutes from midnight, exclusive
    title: str

    def __post_init__(self) -> None:
        if not (0 <= self.start < self.end <= MINUTES_PER_DAY):
            raise ValueError("booking outside 0..1440 range")


@dataclass
class Room:
    name: str
    capacity: int
    bookings: List[Booking] = field(default_factory=list)
    blocked: bool = False


def _booking(start_hm: str, end_hm: str, title: str) -> Booking:
    sh, sm = map(int, start_hm.split(":"))
    eh, em = map(int, end_hm.split(":"))
    return Booking(start=sh * 60 + sm, end=eh * 60 + em, title=title)


ROOMS: List[Room] = [
    Room(
        name="Library Study Room A",
        capacity=6,
        bookings=[
            _booking("09:00", "10:30", "Group project — CS101"),
            _booking("13:00", "14:00", "Faculty meeting"),
            _booking("16:30", "18:00", "Peer tutoring"),
        ],
    ),
    Room(
        name="Engineering Lab B12",
        capacity=24,
        bookings=[
            _booking("11:00", "12:30", "Robotics workshop"),
            _booking("15:00", "17:00", "Senior design review"),
        ],
        blocked=False,
    ),
    Room(
        name="Seminar Room 204",
        capacity=12,
        bookings=[
            _booking("08:30", "09:30", "Office hours"),
            _booking("10:00", "11:00", "Thesis defense"),
        ],
        blocked=True,  # out of service today — AC3 always rejects
    ),
    Room(
        name="Open Collaboration Space",
        capacity=30,
        bookings=[],  # wide open all day
        blocked=False,
    ),
]

# Indices for fast lookup by name.
ROOM_BY_NAME = {r.name: r for r in ROOMS}


# ---------------------------------------------------------------------------
# Pure contract: can_book  (AC1-AC4)  — no side effects
# ---------------------------------------------------------------------------

def can_book(
    start: int,
    end: int,
    now: int,
    blocked: bool,
    existing: List[Booking],
) -> bool:
    """Return True only when AC1-AC4 all hold. Never mutates `existing`."""
    # AC1 — integer minutes, 0 <= start < end <= 1440, start strictly after now
    if not isinstance(start, int) or not isinstance(end, int) or not isinstance(now, int):
        return False
    if not (0 <= start < end <= MINUTES_PER_DAY):
        return False
    if not start > now:  # strictly after now
        return False

    # AC2 — duration at most 120 minutes; exactly 120 is allowed
    duration = end - start
    if duration > MAX_DURATION_MIN:
        return False

    # AC3 — reject every request when the room is blocked
    if blocked:
        return False

    # AC4 — reject overlap with any existing booking;
    # touching at an endpoint is NOT overlap.
    for b in existing:
        if start < b.end and b.start < end:
            return False

    return True


def validate_request(start: int, end: int, now: int) -> Tuple[bool, str]:
    """Friendly, unambiguous validation messages for AC1/AC2 issues (AC6)."""
    if not isinstance(start, int) or not isinstance(end, int):
        return False, "Start and end must be whole minutes."
    if start < 0 or end > MINUTES_PER_DAY:
        return False, "Times must stay within the day (00:00–24:00)."
    if start >= end:
        return False, "End time must be after start time."
    if not start > now:
        return False, "Start time must be strictly in the future."
    if (end - start) > MAX_DURATION_MIN:
        return False, "Bookings may last at most 120 minutes."
    return True, ""


def now_minutes() -> int:
    """Minutes from midnight right now."""
    import datetime
    t = datetime.datetime.now().time()
    return t.hour * 60 + t.minute


def minutes_to_hhmm(m: int) -> str:
    h, mm = divmod(m, 60)
    return f"{h:02d}:{mm:02d}"


# ---------------------------------------------------------------------------
# HTTP layer
# ---------------------------------------------------------------------------

PAGE_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Room Availability Checker</title>
<style>
  :root {
    --bg: #0f172a;
    --card: #1e293b;
    --border: #334155;
    --text: #e2e8f0;
    --muted: #94a3b8;
    --primary: #2563eb;
    --primary-hover: #1d4ed8;
    --success: #16a34a;
    --success-bg: #052e16;
    --error: #dc2626;
    --error-bg: #3b0d0d;
    --warning: #d97706;
    --warning-bg: #3a2607;
    --radius: 12px;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.5;
    min-height: 100vh;
  }
  .wrap {
    max-width: 640px;
    margin: 0 auto;
    padding: 24px 20px 48px;
  }
  h1 {
    font-size: 1.6rem;
    margin: 0 0 4px;
  }
  .sub {
    color: var(--muted);
    font-size: 0.95rem;
    margin: 0 0 20px;
  }
  .card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 18px;
    margin-bottom: 16px;
  }
  label { display:block; font-size: 0.85rem; color: var(--muted); margin-bottom 6px; }
  label { margin-bottom: 6px; }
  select, input[type=number] {
    width: 100%;
    background: #0f172a;
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 1rem;
  }
  select:focus, input:focus { outline: 2px solid var(--primary); }
  .row { display:grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
  .status {
    padding: 10px 14px;
    border-radius: 8px;
    font-weight: 600;
    margin-bottom: 12px;
    display: none;
  }
  .status.ok { background: var(--success-bg); border:1px solid var(--success); color:#bbf7d0; display:block; }
  .status.no { background: var(--error-bg); border:1px solid var(--error); color:#fecaca; display:block; }
  .status.warn { background: var(--warning-bg); border:1px solid var(--warning); color:#fde68a; display:block; }
  .status small { display:block; font-weight:400; margin-top:4px; color: var(--muted); }
  button {
    width: 100%;
    background: var(--primary);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 13px;
    font-size: 1.05rem;
    font-weight: 600;
    cursor: pointer;
    transition: background .15s;
  }
  button:hover { background: var(--primary-hover); }
  button:disabled { opacity: .6; cursor: default; }
  .bookings { list-style:none; padding:0; margin:8px 0 0; }
  .bookings li { padding:6px 0; border-bottom:1px dashed var(--border); font-size:.92rem; }
  .bookings li:last-child { border-bottom:none; }
  summary { cursor:pointer; color: var(--muted); font-size:.9rem; }
  .badge { display:inline-block; padding:4px 10px; border-radius:999px; font-size:.8rem; font-weight:600; }
  .badge.bad { background:var(--error-bg); color:#fecaca; border:1px solid var(--error); }
  .badge.good { background:var(--success-bg); color:#bbf7d0; border:1px solid var(--success); }
  details { margin-top: 14px; }
  details[open] summary { margin-bottom: 8px; }
</style>
</head>
<body>
  <div class="wrap">
    <h1>🏫 Smart Campus Room Availability Checker</h1>
    <p class="sub">Check whether a room is available. This tool only checks availability — it does not create or confirm bookings.</p>

    <div class="card">
      <label for="room">Select a room</label>
      <select id="room"></select>
      <p id="roomMeta" style="margin:10px 0 0;font-size:.9rem;"></p>
    </div>

    <div class="card">
      <details id="bookingsExp">
        <summary>See today's existing bookings</summary>
        <ul class="bookings" id="bookings"></ul>
      </details>
    </div>

    <div class="card">
      <h2 style="font-size:1.05rem;margin:0 0 12px;">When would you like to use the room?</h2>
      <div class="row">
        <div><label>Start hour</label><input type="number" id="sh" min="0" max="23" value="10"></div>
        <div><label>Start min</label><input type="number" id="sm" min="0" max="59" value="0" step="5"></div>
        <div><label>End hour</label><input type="number" id="eh" min="0" max="24" value="11"></div>
        <div><label>End min</label><input type="number" id="em" min="0" max="59" value="0" step="5"></div>
      </div>
      <div style="height:14px"></div>
      <button id="check" type="button">Check availability</button>
    </div>

    <div class="status" id="status"></div>

    <div class="card">
      <details>
        <summary>How availability is decided (the rules)</summary>
        <ul style="margin:8px 0 0;padding-left:18px;font-size:.9rem;color:var(--muted);">
          <li><b>AC1</b> Whole minutes within 00:00–24:00; start must be strictly in the future.</li>
          <li><b>AC2</b> Up to 120 minutes; exactly 120 is allowed.</li>
          <li><b>AC3</b> If the room is blocked, every request is rejected.</li>
          <li><b>AC4</b> Cannot overlap an existing booking; touching endpoints is NOT overlap.</li>
          <li><b>AC5</b> Always an unambiguous Available / Unavailable; nothing is ever created or changed.</li>
          <li><b>AC6</b> Invalid requests get a plain-language explanation.</li>
        </ul>
      </details>
    </div>
  </div>

<script>
let ROOMS = [];
const $ = (id) => document.getElementById(id);

function hhmm(m){ const h=Math.floor(m/60), mm=m%60; return String(h).padStart(2,'0')+":"+String(mm).padStart(2,'0'); }

function renderRooms(rooms){
  ROOMS = rooms;
  const sel = $('room');
  sel.innerHTML = rooms.map(r => `<option value="${r.name}">${r.name}</option>`).join('');
  updateRoomMeta();
  sel.addEventListener('change', updateRoomMeta);
}

function updateRoomMeta(){
  const r = ROOMS.find(x => x.name === $('room').value);
  if(!r) return;
  const meta = $('roomMeta');
  if(r.blocked){
    meta.innerHTML = `<span class="badge bad">Blocked today — no bookings available</span> (capacity ${r.capacity})`;
  } else {
    meta.innerHTML = `<span class="badge good">${r.capacity} seats · ${r.bookings.length} existing bookings</span>`;
  }
  const ul = $('bookings');
  if(r.bookings.length === 0){
    ul.innerHTML = '<li>No bookings — the room is completely open.</li>';
  } else {
    const sorted = [...r.bookings].sort((a,b)=>a.start-b.start);
    ul.innerHTML = sorted.map(b => `<li>• ${hhmm(b.start)} – ${hhmm(b.end)} · ${b.title}</li>`).join('');
  }
}

async function check(){
  const status = $('status');
  status.className = 'status';
  const btn = $('check');
  btn.disabled = true; btn.textContent = 'Checking…';

  const params = new URLSearchParams({
    room: $('room').value,
    sh: $('sh').value, sm: $('sm').value,
    eh: $('eh').value, em: $('em').value,
  });

  try {
    const res = await fetch('/check?' + params.toString());
    const data = await res.json();
    status.className = 'status ' + (data.available === true ? 'ok' : (data.kind === 'warn' ? 'warn' : 'no'));
    if(data.available === true){
      status.innerHTML = `✅ Available: ${data.start_hhmm} – ${data.end_hhmm} (${data.duration} min)
        <small>This is an availability check only — no booking was created.</small>`;
    } else {
      status.innerHTML = `❌ Unavailable — ${data.reason || 'the request did not pass all availability rules.'}`;
    }
  } catch(e){
    status.className = 'status no';
    status.textContent = '❌ Unavailable — could not reach the server.';
  } finally {
    btn.disabled = false; btn.textContent = 'Check availability';
  }
}

$('check').addEventListener('click', check);
fetch('/rooms').then(r=>r.json()).then(renderRooms);
</script>
</body>
</html>
"""


def room_to_dict(r: Room) -> dict:
    return {
        "name": r.name,
        "capacity": r.capacity,
        "blocked": r.blocked,
        "bookings": [{"start": b.start, "end": b.end, "title": b.title} for b in r.bookings],
    }


class Handler(BaseHTTPRequestHandler):
    def _send(self, body: bytes, ctype: str, code: int = 200) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self._send(PAGE_HTML.encode("utf-8"), "text/html; charset=utf-8")
            return

        if path == "/rooms":
            body = json.dumps([room_to_dict(r) for r in ROOMS]).encode("utf-8")
            self._send(body, "application/json")
            return

        if path == "/check":
            self._handle_check(urllib.parse.parse_qs(parsed.query))
            return

        self._send(b"Not found", "text/plain", 404)

    def _handle_check(self, q: dict) -> None:
        def first(name: str, default: str = "") -> str:
            v = q.get(name)
            return v[0] if v else default

        def to_int(name: str) -> int:
            raw = first(name)
            if raw == "":
                return -1
            try:
                return int(raw)
            except ValueError:
                return -1

        room_name = first("room")
        room = ROOM_BY_NAME.get(room_name)

        sh = to_int("sh"); sm = to_int("sm")
        eh = to_int("eh"); em = to_int("em")

        # Normalize "24:00" end (hour=24, min=0) to 1440.
        start = sh * 60 + sm
        end = eh * 60 + em
        if eh == 24 and em == 0:
            end = MINUTES_PER_DAY

        now = now_minutes()

        # If inputs are non-integer/out-of-range, validate_request catches them.
        if room is None:
            self._send(
                json.dumps({"available": False, "kind": "warn",
                            "reason": "Please select a room."}).encode("utf-8"),
                "application/json",
            )
            return

        # Treat clearly invalid integers as validation errors.
        if sh < 0 or sm < 0 or eh < 0 or em < 0:
            ok, msg = False, "Start and end must be whole minutes."
        else:
            ok, msg = validate_request(start, end, now)

        if not ok:
            self._send(
                json.dumps({"available": False, "kind": "warn", "reason": msg}).encode("utf-8"),
                "application/json",
            )
            return

        available = can_book(
            start=start, end=end, now=now,
            blocked=room.blocked, existing=room.bookings,
        )

        if available:
            payload = {
                "available": True,
                "start_hhmm": minutes_to_hhmm(start),
                "end_hhmm": minutes_to_hhmm(end),
                "duration": end - start,
            }
        else:
            if room.blocked:
                reason = "the room is blocked today."
            else:
                clashes = [b for b in room.bookings if start < b.end and b.start < end]
                if clashes:
                    c = clashes[0]
                    reason = (
                        f"it overlaps with '{c.title}' "
                        f"({minutes_to_hhmm(c.start)}–{minutes_to_hhmm(c.end)})."
                    )
                else:
                    reason = "the request did not pass all availability rules."
            payload = {"available": False, "reason": reason}

        self._send(json.dumps(payload).encode("utf-8"), "application/json")

    def log_message(self, *args, **kwargs) -> None:  # quieter console
        pass


def main() -> None:
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Room Availability Checker running: http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()
