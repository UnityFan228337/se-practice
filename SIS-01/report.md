# SIS #01 — Software Engineering Fundamentals, With an AI in the Loop

<!--
  This is the only file you write your report in. README.md tells you what goes where.

  Rules the checker relies on:
  - Do not delete, rename or renumber the ## headings, the ### headings, or the **Label:** words.
  - Replace every "(write here)" and "(paste here)". None may be left when you submit.
  - Comments like this one are ignored by the word counter. Delete them or leave them.
-->

**Topic:** 1.6

<!-- Exactly one of 1.1 … 1.10, e.g.  **Topic:** 1.4  -->

---

## 1. Scenario

<!-- 100–150 words, labels included. One small scenario, used in every prompt and in your
     whole answer. Anything fictional is labelled in Assumptions. -->

**Question:** Which fundamental engineering principles (process management, dependability, understanding requirements, reuse) should a small team prioritise when building a dormitory laundry-booking system in eight weeks?

**Users:** About 400 dorm residents who book washing machines, and two dorm administrators who manage machines and resolve disputes.

**Problem:** Booking currently happens in a Telegram chat. Slots are double-booked, queues are disputed, and broken machines are not tracked.

**Constraints:** 1. Three part-time student developers and eight weeks. 2. No budget: only free university hosting, and data must stay on university servers.

**Risk:** A concurrency bug allows double-booking, or a single user books many slots and blocks others (misuse).

**Assumptions:** The dorm has 12 machines; peak demand is 7–10 pm; residents log in with university accounts; administrators have no technical skills.(fictional)

## 2. Analysis

<!-- 350–400 words. Your answer to the question, the trade-offs, and how it applies to your
     scenario. Explain at least two engineering decisions and why they fit the scenario. -->

(write here)

## 3. Review

<!-- 250–300 words. What Prompt B's critique said and what you did with it; your two source
     checks and your two substantive revisions, each with a reason. Point at the rows of the
     tables in section 9 ("verification row 2", "change-log row 1"). -->

(write here)

## 4. Conclusion

<!-- 100–150 words. Your recommendation for the scenario and its main limitation. -->

(write here)

## 5. Reflection

<!-- 150–200 words. NOT part of the main total. Written by you, not by the assistant:
     what helped, what you changed, what you learned. Specific beats flattering. -->

(write here)

## 6. References

<!-- Full references, one per line, each starting with "- ". Only sources you actually opened.
     Every URL used in the verification table must also appear here. Example:
     - Sommerville, I. (2016). Software Engineering, 10th ed., Global Edition. Pearson. Ch. 1.
-->

- (write here)

## 7. Appendix A — Initial outline

1. Understanding requirements comes first. In week 1 I would talk to a few residents and both administrators to separate must-haves (book/cancel a slot, see availability, report a broken machine, admin override) from nice-to-haves. With only eight weeks, building the wrong features is the biggest waste.

2. Dependability is the top quality goal, specifically correctness and fairness of booking. Double-booking is exactly the problem we are replacing, so the system must prevent it by design (e.g. a database constraint on machine + time slot), and it must stay available during the 7–10 pm peak. A per-user limit on active bookings handles misuse.

3. Process management should be lightweight and incremental: two-week iterations, a prioritised backlog, and a working minimal version by about week 4–5. Then pilot it with one part of the dorm, collect feedback, and fix problems in the remaining weeks. A short risk list (concurrency bug, misuse, a developer unavailable) is reviewed every iteration.

4. Reuse as much as possible, because we have three part-time developers and no budget. Use the university login instead of building our own accounts, free university hosting, and a standard web framework with a transactional database. Building authentication or a calendar from scratch would add risk without adding value.

5. My priority order is requirements, then dependability, then reuse, then process overhead. I would deliberately leave out payments, a native mobile app and fancy analytics. The admin interface must be simple enough for non-technical staff, and the team should test the booking logic with concurrent requests before launch.

## 8. Appendix B — AI exchanges

<!-- Complete prompts and complete responses, as text — never screenshots. Paste each inside
     the fenced block that follows its label. If a response itself contains ``` lines, open
     and close that block with ~~~~ instead. You may add B4, B5 … after B3 if you ran more. -->

### B1 — Draft (Prompt A)

- **Tool:** Claude.ai
- **Model:** Claude Sonnet 5.5
- **Date:** 10.11
- **Purpose:** contextual draft

<!-- Model: the exact model with its version, as the tool shows it (e.g. "GPT-5 Thinking",
     "Claude Sonnet 4.5"). If the tool does not show it, write: not displayed
     Date: YYYY-MM-DD -->

**Prompt:**

```text
## 1. Scenario

<!-- 100–150 words, labels included. One small scenario, used in every prompt and in your
     whole answer. Anything fictional is labelled in Assumptions. -->

**Question:** Which fundamental engineering principles (process management, dependability, understanding requirements, reuse) should a small team prioritise when building a dormitory laundry-booking system in eight weeks?

**Users:** About 400 dorm residents who book washing machines, and two dorm administrators who manage machines and resolve disputes.

**Problem:** Booking currently happens in a Telegram chat. Slots are double-booked, queues are disputed, and broken machines are not tracked.

**Constraints:** 1. Three part-time student developers and eight weeks. 2. No budget: only free university hosting, and data must stay on university servers.

**Risk:** A concurrency bug allows double-booking, or a single user books many slots and blocks others (misuse).

**Assumptions:** The dorm has 12 machines; peak demand is 7–10 pm; residents log in with university accounts; administrators have no technical skills.(fictional)



## 7. Appendix A — Initial outline

1. Understanding requirements comes first. In week 1 I would talk to a few residents and both administrators to separate must-haves (book/cancel a slot, see availability, report a broken machine, admin override) from nice-to-haves. With only eight weeks, building the wrong features is the biggest waste.

2. Dependability is the top quality goal, specifically correctness and fairness of booking. Double-booking is exactly the problem we are replacing, so the system must prevent it by design (e.g. a database constraint on machine + time slot), and it must stay available during the 7–10 pm peak. A per-user limit on active bookings handles misuse.

3. Process management should be lightweight and incremental: two-week iterations, a prioritised backlog, and a working minimal version by about week 4–5. Then pilot it with one part of the dorm, collect feedback, and fix problems in the remaining weeks. A short risk list (concurrency bug, misuse, a developer unavailable) is reviewed every iteration.

4. Reuse as much as possible, because we have three part-time developers and no budget. Use the university login instead of building our own accounts, free university hosting, and a standard web framework with a transactional database. Building authentication or a calendar from scratch would add risk without adding value.

5. My priority order is requirements, then dependability, then reuse, then process overhead. I would deliberately leave out payments, a native mobile app and fancy analytics. The admin interface must be simple enough for non-technical staff, and the team should test the booking logic with concurrent requests before launch.
Act as a software engineering tutor. Help me analyze topic [number and question] for a first-year-level university assignment.

My scenario is [users, problem, constraints and risk]. My initial ideas are [five points]. Draft a 400–500 word explanation using these details.

Separate facts from assumptions. Explain trade-offs and identify claims I should verify. Do not invent quotations, references or page numbers.
```

**Response:**

```text
Engineering principles are not equally valuable in every project, so the real skill is prioritising them for the context. For a dormitory laundry-booking system built by three part-time students in eight weeks with no budget, I would prioritise understanding requirements first, dependability second, reuse third, and keep process management lightweight.

Understanding requirements comes first because, with only eight weeks, the biggest waste is building the wrong thing. The Telegram chat already shows the real problems: double-booked slots, disputed queues, and untracked broken machines. In week 1, short conversations with residents and both administrators let the team separate must-haves (book or cancel a slot, see availability, report a broken machine, admin override) from nice-to-haves. The trade-off is that interviews take time away from coding, so they should be limited to week 1 and then supplemented by pilot feedback.

Dependability is the main quality goal because double-booking is exactly the failure the system replaces. If it still happens, residents will go back to Telegram. The system should prevent it by design, for example with a database uniqueness constraint on machine and time slot, so correctness doesn’t depend only on application code. Availability matters most during the 7–10 pm peak. A cap on active bookings per user addresses misuse, but there is a trade-off: a strict cap reduces slot hoarding yet may frustrate residents with legitimate needs, so administrators should be able to adjust it. Dependability also costs testing time, especially for concurrent requests.

Reuse reduces both risk and effort for a small team. University login, free university hosting, a standard web framework and a transactional database avoid building authentication or calendar logic from scratch, and hosting on university servers also satisfies the data requirement. The trade-off is dependence on things the team doesn’t control: login integration may need approval, and a framework may not fit every need perfectly.

Process management should be lightweight: two-week iterations, a prioritised backlog, a working minimal version by weeks 4–5, a pilot in one part of the dorm, and a short risk list reviewed each iteration. A heavy process would consume scarce time, but too little process risks missed deadlines when a part-time developer is unavailable.

Overall, this ordering fits the context: a small team, a fixed deadline, no budget, and a highly visible failure mode. I would deliberately leave out payments, a native mobile app and analytics. The ordering is context-dependent. In a safety-critical system, dependability would clearly come first, and with a large budget, reuse would matter less.

Facts vs assumptions

Facts (given in your scenario): about 400 residents, two administrators, Telegram-based booking today, three part-time developers, eight weeks, no budget, data must stay on university servers.

Assumptions (label as fictional in your assignment): 12 machines, a 7–10 pm peak, university-account login, non-technical administrators.

Your own judgement (argue, don’t state as fact): the priority order, and that wrong features are the biggest risk.

Claims to verify
Whether your university actually offers single sign-on for student projects, and who approves it.
Whether the free hosting provides a database with transaction and constraint support.
That a uniqueness constraint fully prevents double-booking in your chosen database. Test it with concurrent requests rather than assuming.
Whether two-week iterations and a week 4–5 minimal version are realistic given your part-time hours.
That a per-user booking cap actually reduces misuse. This is an assumption until the pilot gives you evidence.
Your course’s definitions of these four principles. Use your lecture notes or textbook and cite them yourself, since I haven’t given any references.
```

### B2 — Critique (Prompt B)

- **Tool:** (write here)
- **Model:** (write here)
- **Date:** (write here)
- **Purpose:** critical review of the draft

**Prompt:**

```text
(paste here)
```

**Response:**

```text
(paste here)
```

### B3 — Revision (Prompt C)

- **Tool:** (write here)
- **Model:** (write here)
- **Date:** (write here)
- **Purpose:** revision using my decisions and verified evidence

**Prompt:**

```text
(paste here)
```

**Response:**

```text
(paste here)
```

## 9. Appendix C — Evidence tables

### Verification table

<!-- At least two complete rows. Source and locator: title + page / slide / section / chapter,
     or title + URL + access date (YYYY-MM-DD). Decision: keep, qualify or reject — one word. -->

| AI claim | Source and locator | Evidence found | Decision |
| --- | --- | --- | --- |
| (write here) | (write here) | (write here) | (write here) |
| (write here) | (write here) | (write here) | (write here) |

### Change log

<!-- At least two substantive revisions. Your final version must differ from the AI wording,
     and the reason must say which evidence or scenario constraint made you change it. -->

| AI wording / suggestion | Your final version | Reason for change |
| --- | --- | --- |
| (write here) | (write here) | (write here) |
| (write here) | (write here) | (write here) |
