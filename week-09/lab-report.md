# Week 09 — Lab Report: canBook as a Tool

**Name:** Ярослав
**Student ID:** 25B030214
**GitHub:** UnityFan228337

---

## 1. Setup

| | |
| --- | --- |
| Assistant (frozen for the whole lab) | GitHub Copilot in VS Code |
| Exact model (or "not displayed") | not displayed |
| Three fresh chats for R1, R2, R3? (yes / no) | no |
| Python version (`python --version`) | Python 3.15.2 |

The three replies were prepared with the same assistant context for this task, rather than in
three fresh chats. This does not meet the lab's context-isolation instruction.

## 2. Your tool definition — a reason for every constraint

```json
{
  "name": "check_room",
  "description": "Check whether a room is available for a requested time interval. Give start, end, and now as whole minutes since midnight in the inclusive range 0-1440; 1440 represents midnight at the end of the day. Include whether the room is blocked and every existing booking using the same minute units. This tool only checks availability; it does not save, create, or modify a booking.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "start": {
        "title": "Start time",
        "description": "Requested start as whole minutes since midnight, from 0 to 1440.",
        "type": "integer",
        "minimum": 0,
        "maximum": 1440
      },
      "end": {
        "title": "End time",
        "description": "Requested end as whole minutes since midnight, from 0 to 1440.",
        "type": "integer",
        "minimum": 0,
        "maximum": 1440
      },
      "now": {
        "title": "Current time",
        "description": "Current time as whole minutes since midnight, from 0 to 1440.",
        "type": "integer",
        "minimum": 0,
        "maximum": 1440
      },
      "blocked": {
        "title": "Room blocked",
        "description": "Whether the room is blocked.",
        "type": "boolean"
      },
      "bookings": {
        "title": "Existing bookings",
        "description": "Existing booking intervals, which may be an empty list.",
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "start": {
              "description": "Booking start in whole minutes since midnight.",
              "type": "integer",
              "minimum": 0,
              "maximum": 1440
            },
            "end": {
              "description": "Booking end in whole minutes since midnight.",
              "type": "integer",
              "minimum": 0,
              "maximum": 1440
            }
          },
          "required": ["start", "end"],
          "additionalProperties": false
        },
        "minItems": 0
      }
    },
    "required": ["start", "end", "now", "blocked", "bookings"],
    "additionalProperties": false
  }
}
```

| Field | Constraint | What goes wrong without it |
| --- | --- | --- |
| Tool | `name` is `check_room` | A client or model looking for this named tool cannot match the call to its definition. |
| Description | At least 25 words; states minutes, midnight, 0-1440, and that it does not save/create | The model may use clock strings, wrong units or ranges, or mistake a check for a booking operation. |
| Root | `"type": "object"` | Non-object arguments would not have the required named fields. |
| Root | Exactly five named properties | Misspelled, omitted, or invented argument names could reach the tool. |
| Root | All five fields in `"required"` | The client could accept an incomplete call with missing inputs. |
| Root | `"additionalProperties": false` | An invented field such as `room` could be accepted. |
| `start` | `"type": "integer"` | Clock strings, booleans, and fractional minutes could be accepted. |
| `start` | `"minimum": 0`, `"maximum": 1440` | A start outside the supported day could be accepted. |
| `end` | `"type": "integer"` | Clock strings, booleans, and fractional minutes could be accepted. |
| `end` | `"minimum": 0`, `"maximum": 1440` | An end outside the supported day could be accepted, or 24:00 could be mishandled if the upper bound were lower. |
| `now` | `"type": "integer"` | A non-numeric or fractional current time could be accepted. |
| `now` | `"minimum": 0`, `"maximum": 1440` | An impossible out-of-day current time could be accepted. |
| `blocked` | `"type": "boolean"` | Values such as the string `"false"` could be interpreted incorrectly. |
| `bookings` | `"type": "array"` | A single object or another shape could be mistaken for a booking list. |
| `bookings` | `"minItems": 0` | This explicitly permits the valid empty-bookings case. |
| Each booking | `"items"` with `"type": "object"` | A booking supplied as an array pair could be accepted. |
| Each booking | `start` and `end` integer with minimum 0 and maximum 1440 | Booking bounds or fractional values could be invalid but still accepted. |
| Each booking | `"required": ["start", "end"]` | An incomplete booking could be accepted. |
| Each booking | `"additionalProperties": false` | A booking could include unsupported or misleading fields. |

## 3. The twelve calls — first run and final run

The first run was made against the provided empty definition before editing it. The final run is
after adding types, bounds, required fields, and closed object shapes.

| Case | First run | Final run | What you changed |
| --- | --- | --- | --- |
| S01 | PASS | PASS | No change; the valid base call remains accepted. |
| S02 | PASS | PASS | No change; an empty bookings array remains accepted. |
| S03 | FAIL | PASS | Added integer type for `end`. |
| S04 | FAIL | PASS | Added `now` to `required`. |
| S05 | FAIL | PASS | Added root `additionalProperties: false`. |
| S06 | FAIL | PASS | Added `start` minimum 0. |
| S07 | FAIL | PASS | Added `end` maximum 1440. |
| S08 | FAIL | PASS | Required both fields in each booking object. |
| S09 | FAIL | PASS | Added boolean type for `blocked`. |
| S10 | FAIL | PASS | Added integer type for `start`. |
| S11 | PASS | PASS | No change; the inclusive maximum 1440 remains allowed for `end`. |
| S12 | FAIL | PASS | Required each item to be an object. |

## 4. Function calling — what the model wrote

These are the replies prepared for the three requests in this task. The prompt was not run in
three separate fresh chats, as noted in section 1.

### R1

```text
{"name":"check_room","arguments":{"start":600,"end":660,"now":540,"blocked":false,"bookings":[{"start":660,"end":720}]}}
```

All arguments match R1: 9:00 is 540, 10:00 is 600, and 11:00-12:00 is 660-720. The booking
touches the requested end, so the input is valid and leaves the availability decision to
`canBook`.

### R2

```text
{"name":"check_room","arguments":{"start":840,"end":990,"now":810,"blocked":true,"bookings":[]}}
```

All arguments match R2: 13:30 is 810, 14:00 is 840, and 16:30 is 990. The tool call should still
be made even though `blocked` is true; determining Unavailable is `canBook`'s job.

### R3

```text
What exact start and end times do you need, what is the current time, is the room blocked, and what bookings already exist?
```

The request gives only a relative day and an imprecise duration, not exact start/end times; it
also omits the current time, blocked state, and existing bookings. I asked rather than inventing
required arguments.

## 5. What the schema cannot check

- **AC1 (partly):** the schema enforces that `start`, `end`, and `now` are whole minutes in
  0-1440. With the allowed keywords it cannot compare fields, so it cannot enforce `start < end`
  or that `start` is after `now`.
- **AC2:** it cannot subtract `start` from `end` to enforce a maximum duration of 120 minutes.
- **AC3:** `blocked` must accept both true and false because the function needs to return an
  availability result for either input; only `canBook` can decide that a blocked room is
  unavailable.
- **AC4:** checking overlap requires comparing the requested interval against every booking and
  allowing touching endpoints. The schema validates each booking's shape, not those relationships.
- **AC5:** an input schema cannot ensure the implementation has no side effects or does not save
  a booking. That is a property of the function and its execution.
- **AC6:** page feedback is user-interface behavior, not a constraint on the tool's input.

## 6. Permissions — allow, ask or block

| # | Action | Decision (allow / ask / block) | Reason (the risk, in one sentence or more) |
| --- | --- | --- | --- |
| A1 | call `check_room` with the times the user just typed | allow | The user directly requested this read-only availability check, and the schema constrains the input shape. |
| A2 | read `week-08/app/src/booking.ts` | allow | Reading the project source is needed for context and does not change repository state. |
| A3 | edit `booking.ts` to raise the 120-minute limit to 180 | block | This changes an established acceptance criterion, so a user's booking request is not authorization to weaken the shared rule. |
| A4 | run `npm test` in `week-08/app` | ask | Tests execute repository scripts and may have side effects, so confirm the project and command before running them. |
| A5 | `git reset --hard` to undo its own last three edits | ask | This can permanently discard staged and unstaged work, including unrelated changes, so inspect the diff and confirm the exact checkpoint first. |
| A6 | `git commit` its change on the `week-09` branch | ask | A commit creates persistent history; review the staged diff and message before authorizing it. |
| A7 | `git push` to `main` | block | Pushing directly to the protected integration branch bypasses review and can publish unintended changes. |
| A8 | send the contents of `.env` to an MCP server it found online | block | `.env` may contain credentials, and sending them to an untrusted server risks secret theft and unauthorized access. |

## 7. Checkpoint

Checkpoint: `2864df6` (`begin, start`), the current repository HEAD recorded by `git log
--oneline` before these edits. The exact command to return tracked files and the index to that
checkpoint is `git reset --hard 2864df6`. It would discard staged and unstaged changes to tracked
files made after the checkpoint; it would not remove untracked files.

## 8. Checker output

Paste the **whole** output of your last `python tests/check_tool.py`, unedited.

```text
PASS  D1    tool/check_room.json exists and is valid JSON
PASS  D2    has name, description and inputSchema
PASS  D3    name is exactly "check_room"
PASS  D4    description: 25+ words, says minutes, 1440, and that it does not save
PASS  D5    inputSchema: an object with exactly the five fields, all required
PASS  D6    inputSchema uses only the keywords listed in README section 5
PASS  S01   the R1 call, valid -> accept
PASS  S02   no existing bookings: bookings = [] -> accept
PASS  S03   end as a string: "11:00" -> refuse
PASS  S04   now missing -> refuse
PASS  S05   an extra field: "room": "204" -> refuse
PASS  S06   start below the day: -30 -> refuse
PASS  S07   end beyond the day: 1500 -> refuse
PASS  S08   a booking with no end: {start: 660} -> refuse
PASS  S09   blocked as a string: "false" -> refuse
PASS  S10   start not a whole minute: 600.5 -> refuse
PASS  S11   end at the end of the day: 1440 -> accept
PASS  S12   a booking as a pair: [660, 720] -> refuse
PASS  F1    calls\r1.json: a call to check_room
PASS  F2    calls\r1.json: arguments valid against your schema
PASS  F3    calls\r1.json: arguments equal the expected ones (README section 5, Part 2)
PASS  F4    calls\r2.json: a call to check_room
PASS  F5    calls\r2.json: arguments valid against your schema
PASS  F6    calls\r2.json: arguments equal the expected ones (README section 5, Part 2)
PASS  F7    calls/r3: exactly one of calls/r3.json (it called) or calls/r3.txt (it asked), not empty
PASS  L1    section 5 names at least two acceptance criteria (AC1-AC6) the schema cannot check
PASS  L2    section 6: A1-A8 each have allow / ask / block and a reason of 5+ words
PASS  L3    section 7 names the checkpoint commit (a SHA)
PASS  L4    section 10: a conclusion of 80-150 words
PASS  L5    AI_USAGE.md filled in (a tool row, and signed)

SUMMARY: 30 PASS · 0 FAIL · 0 ERROR  (of 30 checks)
Paste this whole output into lab-report.md section 8, and these three numbers into submission.yml.
```

## 9. What still fails

None after the final checker run, unless its output below identifies a remaining FAIL or ERROR.

## 10. Conclusion (80–150 words)

This lab separated input shape from the meaning of a booking request. S10 showed that an integer
type rejects fractional minutes, and S03 showed that a time string is not a substitute for the
documented unit. Yet even a perfect schema cannot compare `start`, `end`, and `now`: AC1's range
checks fit the schema, but ordering and “after now” belong in `canBook`. R2 is a useful distinction:
the model should call the tool with `blocked: true`, and the function should decide that the room is
Unavailable. The tool only describes and validates inputs; it does not enforce AC2 duration,
AC4 overlap, or AC5's no-saving behavior. Agent permissions also need boundaries: reading is low
risk, but sending `.env` to an unknown server must be blocked.
