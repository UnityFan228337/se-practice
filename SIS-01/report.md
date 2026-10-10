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

The team should prioritise understanding requirements first, dependability second, reuse third and a light process last. I ranked them by the project failure each prevents, and by how likely and damaging that failure is. With only eight weeks and three part-time developers, building the wrong features would waste the scarce time, so week 1 goes to talking with a few residents and both administrators and reviewing past Telegram conflicts. Because a few residents out of about 400 is a small sample, the must-have list (book and cancel a slot, see availability, report a broken machine, admin override) is a hypothesis to test in a pilot.

The first engineering decision is a database uniqueness constraint on machine and time slot. It stops two identical bookings, which is the exact problem the Telegram chat has. The PostgreSQL documentation only guarantees uniqueness of values, so it does not solve no-shows or one user holding many slots. For those we add a limit on active bookings and a logged admin override. We assume slots have fixed length, so overlap is not a risk here. Dependability also covers more than correctness (Sommerville, Ch. 10), so availability during the assumed 7-10 pm peak and security of resident data matter. The trade-off is that free university hosting may not guarantee availability, so we should not promise more than it provides.

The second decision is reuse of the university login, free hosting and a standard framework. This saves effort for a team with no budget, but reuse reduces control (Sommerville, Ch. 15). University login is only an assumption, so if IT approval takes longer than two weeks, we start with a simple login limited to dorm residents and switch later.

Process management comes last because a small team can keep it simple. We use two-week iterations, a prioritised backlog and a short risk list (concurrency bug, misuse, a developer becoming unavailable), reviewed every iteration. A working minimal version around week 4-5 is a target, not a proven estimate, so a pilot with clear rules, running alongside Telegram, comes before full launch. Heavy documentation is not worth the time, but a short handover note is, because students may leave after week 8. The trade-off is that this structure takes meeting time away from coding, which matters with only part-time students.


## 3. Review

<!-- 250–300 words. What Prompt B's critique said and what you did with it; your two source
     checks and your two substantive revisions, each with a reason. Point at the rows of the
     tables in section 9 ("verification row 2", "change-log row 1"). -->

Prompt B’s critique raised thirteen concerns about inaccuracies, missing reasoning and unsupported claims. The most important were that the priority order was asserted rather than argued; that process was ranked last yet given substantial content; that a uniqueness constraint does not fully “prevent” double-booking or solve no-shows; and that trade-offs between principles, such as availability on free hosting, were barely discussed. It also flagged the week 4-5 timeline, university login and the booking limit as unsupported.

I accepted most of these. I justified the order by asking which project failure each principle prevents, ranked by likelihood and impact. I reframed process as “right-sized” rather than “overhead”, added the availability-versus-free-hosting conflict, and relabelled “facts” as “given in the scenario”. I moved university login, the timeline and the booking limit into assumptions to verify. I kept the handover idea as a single short note.

Two source checks shaped the two main revisions. Verification row 2 (PostgreSQL) showed that a uniqueness constraint only guarantees unique values, so I narrowed my double-booking claim and dropped the overlap concern because our slots are fixed-length (change-log row 1). Verification row 3 (Sommerville, Ch. 15) supported reuse but also showed lost control, so I added a time-limited fallback login (change-log row 2).

I did not act on one point: the Telegram-bot alternative is worthwhile, but the word limit does not allow covering it well, so I left it out.

The critique helped most by exposing where my reasoning was assumed rather than shown. Its weakness is that it raised many concerns of unequal importance, so I had to judge which ones mattered.

## 4. Conclusion

<!-- 100–150 words. Your recommendation for the scenario and its main limitation. -->

For this dormitory laundry-booking system, I recommend prioritising requirements, then dependability, then reuse, with a light process. The team should confirm the must-have features early, prevent double-booking with a database constraint, add simple fairness rules such as a booking limit, and reuse the university login and hosting where allowed. The main limitation is that several supporting claims are assumptions: the 7-10 pm peak, fixed-length slots, access to university login, and the week 4-5 timeline. Also, the priority order is a judgement, and if team coordination became the biggest risk, process could rank higher. The pilot should test these assumptions before full launch.

## 5. Reflection

<!-- 150–200 words. NOT part of the main total. Written by you, not by the assistant:
     what helped, what you changed, what you learned. Specific beats flattering. -->

The most helpful part was Prompt B. My first draft sounded convincing, but the critique showed that my priority order was only asserted. That made me add a ranking criterion: which project failure each principle prevents, and how likely and damaging it is. Without that, the order would have been just my opinion.

I changed the answer in several ways. I stopped saying a database constraint “prevents” double-booking, because the PostgreSQL documentation only describes uniqueness of values and says nothing about no-shows or users holding many slots. I also removed the overlap concern from the AI revision, since my scenario uses fixed-length slots. For the university login, I replaced the vague “fallback” with a concrete rule: two weeks, then a simple login.

I did not accept everything. The Telegram-bot alternative and detailed documentation advice were good ideas, but there was no space or source for them.

What I learned is that AI output is a hypothesis, not evidence. Several claims (week 4-5, the 7-10 pm peak, university login) had no source, so I kept them as assumptions. I also learned that critiques differ in importance, so I must decide which ones matter for my scenario.

## 6. References

<!-- Full references, one per line, each starting with "- ". Only sources you actually opened.
     Every URL used in the verification table must also appear here. Example:
     - Sommerville, I. (2016). Software Engineering, 10th ed., Global Edition. Pearson. Ch. 1.
-->

- Sommerville, I. (2016). Software Engineering, 10th ed., Global Edition. Pearson. Ch. 10 and Ch. 15.
- PostgreSQL Global Development Group. PostgreSQL Documentation, "Constraints". https://www.postgresql.org/docs/current/ddl-constraints.html (accessed 2026-10-10).

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
- **Date:** 2026-10-10
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
Act as a software engineering tutor. Help me analyze topic  for a first-year-level university assignment.

My scenario is users, problem, constraints and risk. My initial ideas are five points. Draft a 400–500 word explanation using these details.

Separate facts from assumptions. Explain trade-offs and identify claims I should verify. Do not invent quotations, references or page numbers.
```

**Response:**

```text

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

- **Tool:** Claude.ai
- **Model:** Claude Sonnet 5.5
- **Date:** 2026-10-10
- **Purpose:** This review checks my earlier draft explanation against your chosen question and scenario, so you can see where it is weak before you revise it. It identifies inaccuracies and overclaims (such as treating a database constraint as complete protection against double-booking), gaps in reasoning (such as a priority order that is stated but not argued), and vague or unsupported claims (such as the week 4-5 timeline and the availability of university login). For each concern it explains why it matters, how you could verify it, and offers a counterexample or alternative interpretation. It does not rewrite the answer; it prepares you to decide which concerns to fix first.

**Prompt:**

```text
Review the draft below against my chosen question and scenario. Identify inaccuracies, missing reasoning, vague claims and unsupported assumptions.
For each concern, explain why it matters and how I could check it. Include a counterexample or alternative interpretation. Do not rewrite the answer yet.
Question: Which fundamental engineering principles (process management, dependability, understanding requirements, reuse) should a small team prioritise when building a dormitory laundry-booking system in eight weeks?
Scenario: About 400 dorm residents book washing machines, and two dorm administrators manage machines and resolve disputes. Booking currently happens in a Telegram chat; slots are double-booked, queues are disputed, and broken machines are not tracked. Constraints: three part-time student developers, eight weeks, no budget, only free university hosting, and data must stay on university servers. Risk: a concurrency bug allows double-booking, or a single user books many slots and blocks others. Assumptions (fictional): 12 machines; peak demand 7-10 pm; residents log in with university accounts; administrators have no technical skills.
Draft:

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

- **Tool:** Claude.ai
- **Model:** Claude Sonnet 5.5
- **Date:** 2026-10-10
- **Purpose:** This revision applies my own review decisions and the verified source notes to the first draft, so the final answer is more accurate and better argued. It adds an explicit ranking criterion (the project failure each principle prevents, by likelihood and impact), softens overclaims such as treating a database constraint as complete protection against double-booking, and adds the tensions between principles, such as availability versus free hosting. Claims with no supplied evidence (the week 4-5 timeline, the 7-10 pm peak, university login) stay marked as assumptions. A change table shows what was altered and why, and a gaps list shows what still needs checking.

**Prompt:**

```text
Revise the draft using my review decisions and source notes below. Keep the answer relevant to my scenario and preserve uncertainty where evidence is limited.

My decisions: I accepted most of the critique. I will justify the priority order by the project failure each principle prevents, ranked by likelihood and impact. I will reframe process as right-sized instead of overhead, add the availability versus free hosting conflict, and relabel "facts" as "given in the scenario". I will move university login, the week 4-5 timeline and the booking limit into assumptions to verify. I will add logging for the admin override and a short handover note. I reject the Telegram-bot alternative because there is no space and no source for it.
Verified evidence: (1) Sommerville (2016), Ch. 10, Dependable systems: dependability is a set of attributes (availability, reliability, safety, security), not a single property. Decision: keep. (2) PostgreSQL Documentation, "Constraints" (https://www.postgresql.org/docs/current/ddl-constraints.html, accessed 2026-10-10): a unique constraint ensures values in a column or group of columns are unique across rows; it says nothing about overlapping slots or per-user limits. Decision: qualify. (3) Sommerville (2016), Ch. 15, Software reuse: benefits include reduced effort and faster delivery, problems include less control over system evolution. Decision: qualify.
Draft:

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

Show what you changed and why. Use only the sources I supplied. Flag remaining gaps instead of inventing details.

```

**Response:**

```text
Which engineering principles should the team prioritise?

For a dormitory laundry-booking system built by three part-time students in eight weeks with no budget, all four principles matter, but not equally. The Telegram process causes double-booked slots, disputed queues and untracked broken machines. I ranked each principle by the project failure it prevents, and by how likely and damaging that failure is.

1. Understanding requirements comes first. Building the wrong features would waste the scarce eight weeks. In week 1 the team should talk to a few residents and both administrators, and review past chat conflicts, to separate must-haves (book/cancel a slot, see availability, report a broken machine, admin override) from nice-to-haves. Payments, a native app and analytics are left out. Interviews cost time, and a few residents out of about 400 is a small sample, so the must-have list is a hypothesis to test in the pilot.

2. Dependability is the main quality goal. A uniqueness constraint on machine and time slot can prevent two records for the same slot (PostgreSQL documentation), but it does not handle overlapping slots, no-shows or hoarding. Those need extra rules, such as a limit on active bookings and a logged admin override. Dependability is a set of attributes, not one property (Sommerville, Ch. 10), so availability during the assumed 7-10 pm peak and security of resident data also count. Free university hosting may not guarantee availability, so the team should not promise more than the hosting provides.

3. Reuse reduces effort and risk, with limits. University login, free hosting and a standard framework save effort for a small team, but reuse also reduces control (Sommerville, Ch. 15). Whether students may use university login is unverified, so a simple fallback login should be planned.

4. Process management should be right-sized, not minimal. Two-week iterations, a prioritised backlog and a short risk list (concurrency bug, misuse, a developer becoming unavailable) keep three part-time students coordinated. A working version around week 4-5 is a target, not a proven estimate. A pilot alongside Telegram could itself create conflicts, so it needs clear rules. Heavy documentation is not worth it, but short handover notes are, because students may leave after the project.

Priority order: requirements, dependability, reuse, then process. If coordination proved to be the team’s biggest risk, process could rank higher, so this order is a judgement.

Given in the scenario: about 400 residents, two administrators, three developers, eight weeks, no budget, data on university servers. Assumed (fictional): 12 machines, 7-10 pm peak, university login, non-technical administrators.

What I changed and why
Change	Reason
Added a ranking criterion (failure prevented, likelihood, impact)	The order was asserted, not argued.
Renamed “process overhead” to “right-sized process”	Process had real content but was ranked as a cost.
Softened “prevented by design” to “can prevent two records for the same slot”	A constraint does not solve overlap, no-shows or fairness (verification row 2, qualify).
Added the availability vs free hosting tension	Trade-offs between principles were thin.
Added security and privacy to dependability	Supported by Sommerville Ch. 10 (row 1, keep).
Added the reuse downside and a fallback login	Row 3 was qualify: benefits supported, university login not.
Marked the week 4-5 timeline, the pilot and the interview sample as uncertain	No evidence supplied.
Added admin-override logging and handover notes	Critique concerns 10 and 13.
Relabelled “facts” as “given in the scenario”	The scenario is partly fictional.
Not added: Telegram bot alternative	No space within 500 words, no supplied source.
Remaining gaps
The chapter numbers (10 and 15) and the PostgreSQL access date are unconfirmed until you check your book and open the page.
No source supports the week 4-5 timeline, the 7-10 pm peak, the usefulness of a booking limit, or the availability of university login. They remain assumptions.
The word count is an estimate, so check it in a word counter.
```

## 9. Appendix C — Evidence tables

### Verification table

<!-- At least two complete rows. Source and locator: title + page / slide / section / chapter,
     or title + URL + access date (YYYY-MM-DD). Decision: keep, qualify or reject — one word. -->

| AI claim | Source and locator | Evidence found | Decision |
| --- | --- | --- | --- |
| Dependability covers several attributes (availability, reliability, safety, security), not only correctness, so security of resident data also matters. | Sommerville, I. (2016). Software Engineering, 10th ed., Global Edition. Pearson. Ch. 10, Dependable systems. | The chapter presents dependability as a set of attributes, including availability, reliability, safety and security, rather than a single property. | keep |
| A uniqueness constraint on machine + time slot prevents two rows with the same slot, but does not solve fairness problems such as no-shows or hoarding. | PostgreSQL Documentation, "Constraints" (ddl-constraints), https://www.postgresql.org/docs/current/ddl-constraints.html, accessed 2026-10-10. | The documentation describes unique constraints as ensuring that values in a column or group of columns are unique across rows. It says nothing about overlapping slots or per-user limits. | qualify |
| Reusing existing components (login, hosting, framework) reduces effort and risk for a small team. | Sommerville, I. (2016). Software Engineering, 10th ed., Global Edition. Pearson. Ch. 15, Software reuse. | The chapter lists reduced development effort and faster delivery as benefits of reuse, and also problems such as less control over system evolution. | qualify |

### Change log

<!-- At least two substantive revisions. Your final version must differ from the AI wording,
     and the reason must say which evidence or scenario constraint made you change it. -->

| AI wording / suggestion | Your final version | Reason for change |
| --- | --- | --- |
| "A uniqueness constraint on machine and time slot can prevent two records for the same slot (PostgreSQL documentation), but it does not handle overlapping slots, no-shows or hoarding." | "A uniqueness constraint on machine and time slot stops two identical bookings in the database. Because our slots are fixed-length, overlap is not a risk for us, so the remaining dependability problems are no-shows and one user holding many slots." | The PostgreSQL documentation only describes uniqueness of values (verification row 2, qualify). The overlap concern was general, and our scenario uses fixed slots, so I removed it and kept the two fairness problems that the constraint really cannot solve. |
| "Whether students may use university login is unverified, so a simple fallback login should be planned." | "We plan to use university login, but if IT approval takes longer than two weeks, we start with a simple login limited to dorm residents and switch later." | University login is only an assumption in the scenario, and the team has eight weeks, so waiting for approval could block the project. A concrete fallback and a time limit make the risk manageable instead of just naming it. |
| "Process management should be right-sized, not minimal." | "Process management should be light: two-week iterations, a short risk list, and a short handover note, because the team has only three part-time developers and eight weeks." | "Right-sized" is vague and has no support in the supplied sources. Tying the wording to the team size and deadline from the scenario makes the claim specific and checkable. |
