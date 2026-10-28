# SIS #03 — Report: Smart Campus Room Availability Checker

## 1. Setup and reuse

| Item | Value |
| --- | --- |
| Coding assistant (tool) | Bolt.new |
| Coding assistant model | not displayed |
| Bolt.new model | not displayed |
| Bolt project link | https://smart-campus-room-av-p15h.bolt.host |
| Language | Python |
| Path | `app.py` |
| Python v1 from | unavailable in the current project |
| Web v1 from | unavailable in the current project |

The current project contains only the final application files. The original v1 source folders, commit history, screenshots, and submission files are not present, so v1 results are marked as not verifiable rather than invented.

## 2. Baseline — before any new AI exchange

### 2.1 Scope in my own words

**Scope:** One responsive web page lets a student select a fictional room and time slot and see whether it is Available or Unavailable. The page only checks availability and never creates or confirms a booking. Login, persistence, external APIs and payments are outside the scope.

### 2.2 The acceptance criteria in my own words

| AC | In my own words |
| --- | --- |
| AC1 | Times are whole minutes from midnight; start is before end, the end is no later than 1440, and the start is strictly later than the current time. |
| AC2 | A request can last at most 120 minutes; exactly 120 minutes is allowed. |
| AC3 | A blocked room always returns Unavailable. |
| AC4 | Any real overlap with an existing booking is rejected; touching exactly at an endpoint is allowed. |
| AC5 | The result is clearly Available or Unavailable, and checking does not change existing bookings. |
| AC6 | Invalid input receives understandable feedback and the page remains usable on a narrow phone screen. |

### 2.3 Likely failure points

| # | Failure point | AC | How I will check it |
| --- | --- | --- | --- |
| 1 | Treating an endpoint-touching interval as an overlap | AC4 | T1: 660–720 against 600–660 must be Available. |
| 2 | Accepting a start equal to the current time | AC1 | T6: 540–570 with now = 540 must be Unavailable. |
| 3 | Allowing a duration greater than 120 minutes | AC2 | T5: 720–841 must be Unavailable. |
| 4 | Failing to check a second existing booking | AC4 | T10 uses bookings 600–660 and 700–760. |

### 2.4 The contract

| Parameter | Meaning | Type and allowed values |
| --- | --- | --- |
| `start` | requested start, minutes after midnight | integer, 0 through 1439 |
| `end` | requested end, minutes after midnight | integer, greater than start and no greater than 1440 |
| `now` | current time in minutes | integer used as the comparison point |
| `blocked` | whether the room is blocked | boolean |
| `existing` | current bookings | collection of valid `Booking` intervals; never modified |
| returns | whether the request is allowed | `True` only when AC1–AC4 all hold |

### 2.5 Initial assumptions and manual checks

**Assumptions:**

1. Existing bookings are valid intervals with a start before their end.
2. Intervals are half-open: the start is included and the end is excluded.
3. The report's deterministic tests use now = 540 and the listed fixture bookings.

**Checked manually:**

- T1 must be Available because 660 is the end of the existing 600–660 interval, not an overlap.
- T6 must be Unavailable because the start equals now and must be strictly later.
- T11 must give the same result twice and must not change the existing list.

## 3. Python v1 review

The original Python v1 artifact is not included in the current project, so its branches cannot be quoted or reviewed reliably. The final implementation was reviewed instead.

| Branch in v1 (quoted) | AC | Satisfies it? | Why |
| --- | --- | --- | --- |
| v1 source unavailable | AC1 | Not verifiable | The original file is not present. |
| v1 source unavailable | AC2 | Not verifiable | The original file is not present. |
| v1 source unavailable | AC3 | Not verifiable | The original file is not present. |
| v1 source unavailable | AC4 | Not verifiable | The original file is not present. |
| v1 source unavailable | AC5–AC6 | Not verifiable | The original file and its evidence are not present. |

## 4. Prototype v1 in Bolt.new

**Prompt as sent:**

~~~~text
User story: As a student, I want to check a room's availability so that I can choose a valid booking time. One responsive page, one selected room, fictional bookings. Checks availability only - never creates or confirms. Excluded: login, database, backend, external API, payments, unrelated features. AC1 integer minutes: 0 <= start < end <= 1440; start strictly after now AC2 duration at most 120 minutes; exactly 120 is permitted AC3 reject every request when the room is blocked AC4 reject overlap with any booking; touching at an endpoint is NOT overlap AC5 an unambiguous Available / Unavailable; never mutate existing bookings AC6 understandable validation feedback; usable narrow/mobile layout Contract: can_book(start, end, now, blocked, existing) -> True only when AC1-AC4 hold
~~~~

| Generated file or component | Path | Its role |
| --- | --- | --- |
| app.py | `app.py` | Contains the contract, fictional data, HTTP routes and responsive page. |

**What v1 does:**

The original v1 implementation is not available in this project. The final implementation is a standard-library Python HTTP application with one responsive page, a pure availability check, fictional rooms, and no booking mutation.

## 5. Test cases — executed on both artifacts

The final Python contract and final page endpoint were tested with deterministic `now = 540`. The page tests used isolated fixtures so T1–T9 and T11 have existing booking 600–660, while T10 adds 700–760. The v1 artifact was unavailable, and there is no browser renderer in this environment.

| Case | Name | Input | Expected | Python v1 | Python final | Page v1 | Page final |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | Touching | 660–720 | Available | Not testable | Available | Not testable | Available |
| T2 | Overlap | 630–690 | Unavailable | Not testable | Unavailable | Not testable | Unavailable |
| T3 | Blocked | 660–720, blocked | Unavailable | Not testable | Unavailable | Not testable | Unavailable |
| T4 | Exactly 120 min | 720–840 | Available | Not testable | Available | Not testable | Available |
| T5 | 121 min | 720–841 | Unavailable | Not testable | Unavailable | Not testable | Unavailable |
| T6 | Starts now | 540–570 | Unavailable | Not testable | Unavailable | Not testable | Unavailable |
| T7 | Reversed | 720–660 | Unavailable | Not testable | Unavailable | Not testable | Unavailable |
| T8 | Ends at midnight | 1380–1440 | Available | Not testable | Available | Not testable | Available |
| T9 | Past midnight | 1380–1441 | Unavailable | Not testable | Unavailable | Not testable | Unavailable |
| T10 | Second booking | 720–780, existing (600–660), (700–760) | Unavailable | Not testable | Unavailable | Not testable | Unavailable |
| T11 | Same check twice | 660–720, twice | Available | Not testable | Available | Not testable | Available |
| T12 | Narrow screen | T1 at ~375 px wide | Available | n/a | Available | n/a | Available |

T12 was verified by checking the returned page source for the mobile media rule and the two-column narrow-screen layout. A real 375 px visual browser render was not available, so this is source-level evidence rather than a screenshot-based claim.

## 6. Traceability

| AC | Implementation / file | Test input | Expected | v1 actual | Final actual |
| --- | --- | --- | --- | --- | --- |
| AC1 | `app.py`: `can_book` range, integer and future-start checks; `validate_request` messages | T6, T7, T8, T9 | T6/T7/T9 Unavailable; T8 Available | Not testable | Passed: T6/T7/T9 Unavailable; T8 Available |
| AC2 | `app.py`: duration check against `MAX_DURATION_MIN = 120` | T4, T5 | T4 Available; T5 Unavailable | Not testable | Passed |
| AC3 | `app.py`: `if blocked: return False` and page reason | T3 | Unavailable | Not testable | Passed |
| AC4 | `app.py`: half-open overlap expression in `can_book` | T1, T2, T10 | T1 Available; T2/T10 Unavailable | Not testable | Passed |
| AC5 | `app.py`: JSON result and no mutation of `existing` | T11 | Available twice | Not testable | Passed; both calls Available and fixture unchanged |
| AC6 | `app.py`: validation messages and `@media (max-width: 520px)` layout | T12 | Available and usable at about 375 px | Not testable | Source-level mobile rule verified; endpoint behavior passed |

## 7. Issue log

The original v1 file and its evidence are missing, so functional defects cannot be attributed to v1. The following issues were found while completing and verifying the current final artifact.

| # | Issue | Reproduction | Priority | Prompt / change | Retest result |
| --- | --- | --- | --- | --- | --- |
| 1 | Narrow screens originally kept four small time-input columns | AC6, T12 | Medium | Add a mobile breakpoint at 520 px and switch the time grid to two columns. | Source check confirmed the mobile rule and two-column layout. |
| 2 | The page heading included an emoji despite the requested plain interface style | AC6 | Low | Remove the decorative emoji from the heading. | Page source contains the plain heading and still serves successfully. |

**Before / after:** Screenshot evidence is not available in the current project. The responsive CSS change is recorded in `app.py` and verified by reading the served page source.

## 8. Critique decisions

| # | AI claim or recommendation | How I verified it | Decision | Reason (AC or case) |
| --- | --- | --- | --- | --- |
| 1 | Touching an existing booking should be allowed. | Ran T1 through the final contract and `/check` endpoint with 600–660 and 660–720. | Accept | Both returned Available, satisfying AC4. |
| 2 | A start equal to now should be rejected. | Ran T6 with now = 540 and start = 540. | Accept | Both final paths returned Unavailable, satisfying AC1. |
| 3 | The original final page already had a narrow-screen layout suitable for 375 px. | Read the CSS and found a four-column grid with no narrow-screen breakpoint before the repair. | Modify | The claim was too strong; the mobile breakpoint was added before recording the final result. |
| 4 | v1 and final results can be reported as identical. | Checked the project files and found no v1 source or executable test artifact. | Reject | The comparison cannot be honestly made without the missing artifact. |

## 9. Coding-agent analysis

### 9.1 The loop

| Step | What happened in this assignment |
| --- | --- |
| User goal | Complete the SIS report for the room availability checker. |
| Model / plan | Inspect the available project, verify the final implementation, repair the narrow-screen layout, and fill the report without inventing missing evidence. |
| Tool call | Read `app.py`, `README.md` and `requirements.txt`; edited the responsive CSS and heading; ran deterministic contract and HTTP checks. |
| Observation | T1–T11 matched the expected final results. The project did not contain v1 artifacts or screenshots. |
| Next step | Record v1 as not testable, document the final evidence, and state the browser-render limitation. |
| Human review | The report should be checked against the actual submission requirements before submission, especially the missing v1 and screenshot evidence. |

### 9.2 Context, tools and permissions

| Tool | Context it used | Tools or permissions | Observed or assumed |
| --- | --- | --- | --- |
| File reader | Current project files | Read-only access to source and documentation | Observed |
| File editor | Final page source | Permission to modify the local project | Observed |
| Python test run | Deterministic contract and HTTP fixtures | Local process execution and localhost networking | Observed |
| Browser renderer | Not available in this environment | No screenshot or visual viewport tool | Observed |
| Supabase | Not needed for this scoped, fictional, non-persistent checker | No database calls were made | Observed |

### 9.3 Checkpoint and dependability

**Safety checkpoint:** I did not claim v1 behavior, screenshots, commits, or a real browser rendering that were not present or observable. The only source change was a reversible responsive-layout adjustment and removal of the decorative heading emoji.

**Reliability, security, responsibility:** The availability rule is pure and does not mutate bookings. User input is parsed at the HTTP boundary and invalid values receive visible messages. The application has no login, stored personal data, payments, external API calls, or user-supplied HTML content. A future version with persistent data would need server-side access controls and database policies.

## 10. Reflection

AI-assisted coding was useful for turning the acceptance criteria into a small Python contract and for checking boundary cases such as touching intervals, exactly 120 minutes, and a start equal to now. Vibe coding was useful for quickly producing a complete page, but it carried a usability risk: the original four-column time form was too cramped for a narrow phone. Reliability still depends on running the exact cases instead of trusting a plausible-looking result; the endpoint and overlap rules were checked directly. Availability and usability also need a real browser viewport check, which was not available here. Security remains a human responsibility because a future database-backed version would need access rules and validation beyond the current in-memory scope. I rejected the claim that the missing v1 artifact could be reported as tested, because the project did not contain it. Next I would add the missing historical artifacts and run the final page in a real 375 px browser viewport without expanding the product scope.

## 11. Appendix A — AI exchanges

### B1

- **Tool:** Bolt.new
- **Model:** not displayed
- **Date:** 2026-10-28
- **Stage:** Plan
- **Source:** this SIS

**Prompt:**

~~~~text
Review the supplied SIS #03 handout and report template. Complete the report using only evidence present in the current project. Do not invent v1 files, screenshots, commits, or test results.
~~~~

**Response:**

~~~~text
Inspect the current application and documentation first, run the deterministic contract and page checks, make only the necessary responsive repair, then fill every report section while marking unavailable historical evidence as not testable.
~~~~

### B2

- **Tool:** Bolt.new
- **Model:** not displayed
- **Date:** 2026-10-28
- **Stage:** Generate
- **Source:** this SIS

**Prompt:**

~~~~text
As a student, I want to check a room's availability so that I can choose a valid booking time. Use one responsive page, fictional bookings, and availability checks only. Enforce integer minutes, future start, maximum 120 minutes, blocked-room rejection, non-overlapping bookings with endpoint touching allowed, clear feedback, and no booking mutation.
~~~~

**Response:**

~~~~text
The current app provides a standard-library Python HTTP server, a pure can_book function, fictional room data, /rooms and /check routes, clear Available or Unavailable feedback, and a responsive single page. The current source was inspected before final verification.
~~~~

### B3

- **Tool:** Bolt.new
- **Model:** not displayed
- **Date:** 2026-10-28
- **Stage:** Critique
- **Source:** this SIS

**Prompt:**

~~~~text
Check the final implementation against T1–T12 and identify any unsupported claims, especially the narrow-screen behavior and any missing historical v1 evidence.
~~~~

**Response:**

~~~~text
The deterministic final checks pass T1–T11. The project does not contain the original v1 source or screenshots, so those results cannot be claimed. The original four-column form needs a narrow-screen breakpoint before T12 can be reported as verified from source.
~~~~

### B4

- **Tool:** Bolt.new
- **Model:** not displayed
- **Date:** 2026-10-28
- **Stage:** Repair
- **Source:** this SIS

**Prompt:**

~~~~text
Repair only the narrow-screen layout and remove the decorative heading emoji. Keep the availability behavior and scope unchanged.
~~~~

**Response:**

~~~~text
The final page now switches the time inputs to a two-column grid below 520 px and keeps the same availability behavior. The heading is plain text. The served source was checked for the responsive rule, and deterministic endpoint tests still pass.
~~~~

## 12. Appendix B — Test output

### 12.1 Your suite

~~~~text
T1 Available
T2 Unavailable
T3 Unavailable
T4 Available
T5 Unavailable
T6 Unavailable
T7 Unavailable
T8 Available
T9 Unavailable
T10 Unavailable
T11 Available Available
T12 responsive media True two-column mobile grid True
~~~~

The final contract was also run directly with the same expected outcomes for T1–T11. The page endpoint was tested with isolated fixtures and deterministic now = 540.

### 12.2 Path B only — three faults you planted

No Path B fault-planting artifact is present in the current project, and no faults were deliberately planted during this verification. The table therefore records the evidence status rather than inventing failed tests.

| # | Line you broke | AC | Test that failed |
| --- | --- | --- | --- |
| 1 | Not available | Not available | Not available |
| 2 | Not available | Not available | Not available |
| 3 | Not available | Not available | Not available |

## 13. Remaining limitations and known fails

| Check ID or limitation | Why it stays | What I would do next |
| --- | --- | --- |
| Missing Python v1 artifact | The current project contains only the final `app.py`; the original v1 source was not supplied. | Restore the historical v1 artifact from the project history or submission package, then rerun T1–T11. |
| Missing Web v1 artifact | The original web v1 export is not present. | Restore the web v1 artifact and repeat the page checks. |
| No screenshot evidence | This environment has no browser screenshot tool. | Run the final page at approximately 375 px and attach before/after evidence. |
| No Path A unittest suite | The current project has no `tests/` directory or unittest suite. | Add the required test file and run it with the required command before submission. |
| No Path B planted-fault evidence | No fault-planted copy or fault log is present. | Restore or create the required educational fault-testing artifacts, then record the failed cases. |
| No commit/push evidence | The current workspace is not a git repository. | Use the course submission workflow to create the required commits and push if required. |
