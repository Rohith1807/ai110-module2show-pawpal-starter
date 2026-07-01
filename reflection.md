# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

    1. **Add a Pet and its core tasks** (walks, feeding, meds, grooming) with duaration and priority.
    2. **Set daily constraints** (how much time the owner has available today)
    3. **Generate and view today's plan** with reasoning for why tasks were included or skipped.

- What classes did you include, and what responsibilities did you assign to each?

    I chose 4 classes: **Owner, Pet, Task, and Scheduler**
    **Owner** holds the user's info and available time for the day.
    **Pet** hold the identity info and its list of care tasks.
    **Task** represents a single care item with duration and priority so it can be scheduled.
    **Scheduler** is sepearte from the pet because scheduling logic is a behaviour, not a property of the pet itself, and keeping it seperate makes it easier to test and change immediately.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

    After reviewing the skeleton with AI feedback, I made three changes. 
    First, I added an owner back-reference on Pet so scheduling logic can access owner-level constraints without needing to pass the owner separately. 
    Second, I replaced name-based task removal with a unique id field on Task, since two tasks could easily share a name (e.g. two "Walk" entries for morning and evening). 
    Third, I changed Scheduler to operate on the whole Owner instead of a single Pet. 
    My original design didn't account for owners with multiple pets competing for the same block of time, which is actually the more realistic and interesting scheduling problem. I also updated filter_by_time to return both scheduled and skipped tasks explicitly, instead of silently dropping tasks that don't fit, so the app can later show the user what got cut and why.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

    My scheduler considers two constraints: how much time the owner has available today, and each task's priority level (high, medium, low). Duration also factors in indirectly, since it determines whether a task fits in the remaining time budget. I decided time and priority mattered most because they're the two things a real pet owner is actually juggling every morning: "how long do I have" and "what absolutely cannot slip today." Things like owner preferences or pet mood weren't included, since they'd need a way to be expressed and weighted that was out of scope for this build.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

    My conflict detection only checks for exact matches on scheduled_time, not overlapping durations. A 30-minute task starting at 08:00 and a 20-minute task starting at 08:15 actually overlap in real life, but my scheduler won't catch that since neither task's start time equals the other's. I chose this because true overlap detection means converting every time into a start/end range and checking interval overlap, which is meaningfully more code for a first pass. Exact-match detection catches the most obvious case (two tasks scheduled for literally the same time) and keeps the logic easy to read, at the cost of missing partial overlaps.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

    I used AI throughout the project for design brainstorming, code generation, debugging, and refactoring. It was most useful for reviewing my class skeletons and pointing out missing relationships I hadn't noticed, like the missing Owner back-reference on Pet and the fact that my Scheduler only handled one pet at a time. The most helpful prompts weren't "write this feature" but "what's missing or fragile in what I already have," since that's where the actual design gaps showed up. Asking for one method at a time, instead of the whole system at once, also made it easier to catch problems early rather than after a large batch of generated code.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

    When I asked AI to simplify sort_by_time for readability, it suggested collapsing the method into a one-line lambda assigned to a class attribute. I didn't accept that, since a lambda without a docstring is harder to maintain and debug than a named method, especially in a system I planned to keep extending with sorting variations. I verified this by weighing it against how the codebase would need to grow, more sorting logic was coming in later phases, and decided the small readability gain wasn't worth losing the ability to document the method clearly.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

    I tested sorting correctness (tasks return in chronological order, with unscheduled tasks pushed to the end), filtering by pet name and by completion status, recurrence logic (completing a daily task creates a correctly dated next occurrence, one-off tasks don't), and conflict detection (same-time tasks get flagged, different-time tasks don't, and unscheduled tasks don't crash the check). These mattered because they're the exact behaviors a user would notice breaking, silently wrong sort order or a recurring task that never comes back would undermine the whole point of the app.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

    I'm confident the core logic works correctly, all 10 tests pass against the real implementation. My confidence is limited by the known gap in conflict detection, which only catches exact time matches and not overlapping durations. If I had more time, I'd test partial time overlaps directly, what happens when an owner has zero available minutes, and what happens when a pet has a task with a malformed or missing scheduled_time string.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    I'm most satisfied with how the Scheduler ended up structured. Splitting collect, sort, filter, and conflict detection into separate methods made each piece easy to test on its own, and it meant adding new scheduling behavior later (like the priority sort and then the time sort) didn't require touching unrelated code.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    I'd redesign conflict detection to check for actual time overlaps instead of exact matches. I'd also add validation on Task's priority and scheduled_time fields, since right now a typo like "hi" instead of "high" would silently fall through the priority sort without any warning.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    The biggest thing I learned is that AI is very good at generating and fixing code once I've decided what the system should do, but the actual architectural decisions, like whether Scheduler should own one pet or the whole owner, are still mine to make. AI can point out that a decision has consequences, but it can't decide for me which consequence I'm willing to accept for this specific app.