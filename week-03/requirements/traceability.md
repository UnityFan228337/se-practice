# Traceability — use cases → stories → criteria

One row per use case. All six rows stay, even the ones with nothing behind them: an empty cell is a
finding you report, not a failure you hide. Use real IDs, comma-separated; write `none` where there
is nothing.

| Use case | Stories (US-nn) | Criteria (AC-nn) | Gap? |
| --- | --- | --- | --- |
| UC-01 View availability | US-01 | AC-01, AC-02, AC-03 | No gap |
| UC-02 Book room | US-02 | AC-04, AC-05, AC-06, AC-07, AC-08 | No gap |
| UC-03 Cancel booking | US-03 | AC-09, AC-10, AC-11 | No gap |
| UC-04 Block or unblock room | US-04, US-05 | AC-03, AC-08 | No gap |
| UC-05 Review usage | US-06 | none | Criterion gap |
| UC-06 Send confirmation | US-07 | none | Criterion gap |

**Stories that belong to no use case:** none

**What the gaps tell you:** While all six use cases are covered by corresponding user stories, acceptance criteria were explicitly written for only three selected stories (US-01, US-02, US-03) as required by the assignment guidelines, leaving UC-05 and UC-06 without dedicated testing criteria in `acceptance-criteria.md`.