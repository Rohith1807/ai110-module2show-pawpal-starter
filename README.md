# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```bash
==================================================
Today's Schedule for Rohith
Available time: 60 minutes
==================================================
1. [HIGH  ] Biscuit    Morning walk         (30 min)
2. [HIGH  ] Biscuit    Feeding              (10 min)
3. [MEDIUM] Whiskers   Litter box cleaning  (15 min)

Total time used: 55/60 minutes

Skipped (not enough time today):
  - Whiskers: Playtime (20 min)
==================================================
```

## 🧪 Testing PawPal+

Run the full test suite:

    python -m pytest

These tests cover:
- **Sorting correctness** — tasks are returned in chronological order by scheduled time, with unscheduled tasks placed last
- **Filtering** — by pet name and by completion status
- **Recurrence logic** — completing a daily task automatically creates the next day's occurrence, one-off tasks do not
- **Conflict detection** — two tasks scheduled at the same time are flagged with a warning, without crashing the program
- **Edge case** — a pet with zero tasks doesn't break sorting or filtering

```bash
========================================================== test session starts ===========================================================
platform win32 -- Python 3.14.5, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\rohit\OneDrive - University of St. Thomas\codepath\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 10 items                                                                                                                        

tests\test_pawpal.py ..........                                                                                                     [100%]

=========================================================== 10 passed in 0.06s ===========================================================
```

Confidence Level - ★★★★

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature           | Method(s)                          | Notes                                                        |
| ------------------ | ----------------------------------- | ------------------------------------------------------------- |
| Task sorting       | `Scheduler.sort_by_priority()`, `Scheduler.sort_by_time()` | Priority sort tiebreaks on duration; time sort treats unscheduled tasks as end-of-day |
| Filtering          | `Scheduler.filter_tasks()`          | Filters by pet name and/or completion status independently |
| Conflict handling  | `Scheduler.detect_conflicts()`      | Exact time-match detection only, does not catch overlapping durations |
| Recurring tasks    | `Task.next_occurrence()`, `Pet.complete_task()` | Daily/weekly frequency, uses `timedelta` to compute next due date |

## ✨ Features

- **Multi-pet support** — one owner can manage multiple pets, each with their own task list
- **Priority-based scheduling** — `Scheduler.generate_plan()` fills the owner's available time with the highest-priority tasks first
- **Time-based sorting** — `Scheduler.sort_by_time()` orders tasks chronologically, with unscheduled tasks placed last
- **Filtering** — `Scheduler.filter_tasks()` filters by pet or by completion status
- **Conflict warnings** — `Scheduler.detect_conflicts()` flags tasks scheduled at the exact same time so the owner can catch double-booking before the day starts
- **Daily and weekly recurrence** — `Task.next_occurrence()` automatically generates the next instance of a recurring task when the current one is marked complete

## 📸 Demo Walkthrough

1. The owner enters their name and how many minutes they have available today.
2. The owner adds one or more pets by name and species.
3. For each pet, the owner adds care tasks with a title, duration, priority, scheduled time, and frequency (one-time, daily, or weekly).
4. The app displays all tasks sorted by time, with a filter to view a single pet's tasks or hide completed ones.
5. If two tasks share the same scheduled time, a warning appears immediately, naming both tasks and the conflicting time.
6. The owner clicks "Generate schedule." The Scheduler sorts remaining tasks by priority and fills the available time budget, showing which tasks made the cut and which were skipped for lack of time.
7. The owner can mark any task complete. If it's a daily or weekly task, the next occurrence is created automatically and its due date is shown.
