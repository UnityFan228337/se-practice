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

Prompt B’s critique reviewed my first draft and raised thirteen concerns, grouped into inaccuracies, missing reasoning, and vague or unsupported claims. The most important points were that the priority order (requirements, dependability, reuse, process) was asserted rather than argued; that process was ranked last yet given substantial content, which was inconsistent; that a database uniqueness constraint does not fully “prevent” double-booking or solve fairness problems like no-shows; and that trade-offs between principles, such as high availability on free hosting, were barely discussed. It also flagged unsupported claims: the week 4-5 timeline, the availability of university login, and the per-user booking limit.

I did not accept every concern equally. I kept the overall priority order but decided to justify it by asking which project failure each principle prevents, ranked by likelihood and impact. I accepted the inconsistency about process and reframed it as “right-sized process” rather than “overhead.” I softened the double-booking claim to say a constraint prevents duplicate slot records, while fairness needs extra rules. I added one explicit conflict between principles (availability versus free hosting) and relabelled “facts” as “given in the scenario.” I moved the university login, the timeline and the booking limit into a “to verify” list rather than presenting them as certain.

I deliberately did not act on some points. Documentation for handover and the Telegram-bot alternative are worthwhile ideas, but the word limit makes it impossible to cover them well, so I mention them only briefly as alternatives.

The critique helped most by exposing where my reasoning was assumed rather than shown. Its weakness is that it raised many concerns of unequal importance, so I had to judge which ones mattered for the question.

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
- **Purpose:** This answer examines which fundamental software engineering principles a small team should prioritise when building a dormitory laundry-booking system within eight weeks. It uses a small scenario (about 400 residents, two administrators, three part-time developers, no budget) to show how process management, dependability, understanding requirements and reuse compete for limited time, and why they should not be weighted equally. It argues for a priority order (requirements, dependability, reuse, then lightweight process), explains the trade-offs behind it, and separates facts from assumptions so the reader can see which claims still need to be verified.

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
# Draft explanation (about 450 words)

## Which engineering principles should the team prioritise?

For a dormitory laundry-booking system built by three part-time student developers in eight weeks, the core software engineering principles are all relevant, but they do not deserve equal weight. The team has little time, no budget, and a very specific failure to fix: Telegram bookings lead to double-booked slots and disputes. This points to a clear order of priorities.

**1. Understanding requirements comes first.** With eight weeks, building the wrong thing is the costliest mistake. In week 1 the team should talk to a few residents and both administrators to separate must-haves (book and cancel a slot, see availability, report a broken machine, admin override) from nice-to-haves. Payments, a native mobile app and analytics are deliberately left out. The trade-off is that early interviews consume time that could go into coding, but they reduce the risk of rework later.

**2. Dependability is the main quality goal, specifically correctness and fairness of booking.** Double-booking is the exact problem the system replaces, so it should be prevented by design, for example with a database uniqueness constraint on machine and time slot, plus a limit on each user's active bookings to stop misuse. The system must also stay available during the assumed 7-10 pm peak. The trade-off is that strict limits protect fairness but may frustrate residents with legitimate needs, so an admin override is necessary.

**3. Reuse reduces risk and effort.** Using the university login, free university hosting, a standard web framework and a transactional database avoids building authentication or scheduling from scratch. This also helps meet the constraint that data stays on university servers. The trade-off is less control and dependence on what the university provides.

**4. Process management should stay lightweight.** Two-week iterations, a prioritised backlog, a working minimal version by about week 4-5, and a pilot with part of the dorm let the team learn early. A short risk list (concurrency bug, misuse, a developer becoming unavailable) is reviewed each iteration. Heavy documentation would cost more than it gives for a team this small.

**Overall priority order:** requirements, dependability, reuse, then process overhead. The principles also support each other: clear requirements define what "fair" means, and reuse frees time for testing the booking logic with concurrent requests before launch.

## Facts vs assumptions

**Facts (from the scenario):** about 400 residents, two administrators, three part-time developers, eight weeks, no budget, data on university servers, current Telegram-based booking with double-booking and disputes.

**Assumptions (labelled fictional):** 12 machines, peak demand 7-10 pm, university-account login, non-technical administrators.

## Claims to verify

- That the university offers a login system (e.g. single sign-on) the team is actually allowed to use.
- That the free hosting supports a transactional database and enough capacity for peak load.
- That residents and administrators really rank these features as must-haves; the list is currently your hypothesis.
- That a working version by week 4-5 is realistic for part-time developers.
- That a per-user booking limit is acceptable to residents; test it in the pilot.

I have not included any quotations or references. For the assignment, cite your course textbook or lecture notes for the definitions of dependability, requirements engineering and reuse, and check the exact wording there yourself.
```

### B2 — Critique (Prompt B)

- **Tool:** Claude
- **Model:** Claude Sonnet 5.5
- **Date:** 10.11
- **Purpose:** This review checks my earlier draft explanation against your chosen question and scenario, so you can see where it is weak before you revise it. It identifies inaccuracies and overclaims (such as treating a database constraint as complete protection against double-booking), gaps in reasoning (such as a priority order that is stated but not argued), and vague or unsupported claims (such as the week 4-5 timeline and the availability of university login). For each concern it explains why it matters, how you could verify it, and offers a counterexample or alternative interpretation. It does not rewrite the answer; it prepares you to decide which concerns to fix first.

**Prompt:**

```text
Review the draft below against my chosen question and scenario. Identify inaccuracies, missing reasoning, vague claims and unsupported assumptions.
For each concern, explain why it matters and how I could check it. Include a counterexample or alternative interpretation. Do not rewrite the answer yet.
Question: [paste]. Scenario: [paste]. Draft: [paste the full Prompt A response].
```

**Response:**

```text
I filled your placeholders from this conversation: your question and scenario from your first message, and my earlier draft as the draft. Some of these concerns also trace back to your outline, so they are not only flaws in my draft.

## Inaccuracies and overclaims

**1. "Prevented by design" with a uniqueness constraint**
- *Why it matters:* A constraint on machine + time slot stops duplicate rows, but not overlapping slots of different lengths, bookings on a machine that later breaks, or no-shows. Calling this "dependability by design" overstates what it covers.
- *Check:* Write down every way two residents could end up with the same machine at the same time, and test with simultaneous requests.
- *Alternative:* If slots are fixed-length, the constraint is enough for double-booking, and the real dependability problem is fairness (no-shows, hoarding), which a constraint cannot solve.

**2. Telegram "leads to" double-booking**
- *Why it matters:* The root cause may be the lack of one authoritative record rather than Telegram itself. That changes what the new system must do.
- *Check:* Review a sample of past chat history and count actual conflicts and their causes.
- *Alternative:* A Telegram bot over a database would also fix the problem and keep residents' existing habit. The draft never considers this under reuse.

**3. Word count and "facts"**
- *Why it matters:* I stated about 450 words without counting, and the draft may exceed 500. Also, "facts from the scenario" are only facts inside a partly fictional scenario, so labelling them "facts" could mislead a marker.
- *Check:* Paste the draft into a word counter. Relabel the section "given in the scenario" versus "assumed".

## Missing reasoning

**4. The priority order is asserted, not argued**
- *Why it matters:* The assignment asks which principles to prioritise, so the justification for the order is the core of the answer.
- *Counterexample:* If the main requirement is "no double-booking," then requirements and dependability are nearly the same thing, and ranking one above the other is arbitrary. Alternatively, with three part-time students, coordination failure may be the biggest risk, which would put process first.
- *Check:* Ask what concrete project failure each principle prevents, then rank by likelihood times impact.

**5. Process is ranked last, but the draft gives it substantial content**
- *Why it matters:* "Process overhead" treats process management as a cost, while the draft's own process section (iterations, risk list, pilot) is valuable. That is internally inconsistent.
- *Check:* Compare the length and importance you give each principle with its rank.

**6. Trade-offs between principles are thin**
- *Why it matters:* The draft mostly gives trade-offs within each principle. Conflicts between principles (reuse versus control, dependability versus the eight-week limit) are barely discussed.
- *Alternative:* Demanding high availability while using free hosting with no guarantees is a real tension the draft never names.

**7. Dependability is treated narrowly**
- *Why it matters:* It covers correctness and availability but not security or privacy, which matter for resident data and for misuse.
- *Check:* Compare against your course's definition of dependability (reliability, availability, safety, security) and see which attributes apply.

## Vague or unsupported claims

**8. "Building the wrong features is the biggest waste"**
- *Why it matters:* This is an assumption stated as fact. Interviewing "a few" residents out of 400 is a small, possibly biased sample.
- *Counterexample:* The problem is already clear from the Telegram history, so interviews may add little compared with analysing that chat.
- *Check:* Find a requirements-engineering source in your course materials on cost of late changes.

**9. "Working version by week 4-5" and a partial pilot**
- *Why it matters:* There is no basis for this timeline. A pilot with only part of the dorm also means two systems running at once, which could create new double-bookings.
- *Alternative:* Pilot with all residents for one machine, or run a short parallel trial with clear rules.

**10. "Heavy documentation costs more than it gives"**
- *Why it matters:* Student teams graduate, so maintenance and handover may need documentation.
- *Check:* Ask who will maintain the system after week 8.

**11. The reuse section assumes university login is available**
- *Why it matters:* Your scenario lists this as an assumption, but the draft builds its reuse argument on it. Integration can also need IT approval, which could take longer than a simple custom login.
- *Check:* Ask university IT about single sign-on access and lead time.

**12. The per-user booking limit**
- *Why it matters:* It is presented as the solution to misuse without a number or rule. Shared or multiple accounts could bypass it, and no-show penalties may address misuse better than limits.
- *Check:* Test candidate rules in the pilot and see what residents report.

**13. Admin override**
- *Why it matters:* It protects usability, but without logging it can undermine the fairness the system is meant to provide.

When you're ready, tell me which concerns you want to address first and I'll help you revise the draft accordingly.
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
