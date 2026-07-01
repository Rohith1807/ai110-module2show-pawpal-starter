# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the agent to add a third algorithmic capability to `pawpal_system.py`: a method that finds the next available open time slot of a given duration, considering tasks I'd already scheduled, without building a full interval-tree data structure. I wanted something that could eventually power a "suggest a time" feature in the UI when adding a new task.

**What did the agent do?**

The agent added two things to the `Scheduler` class in `pawpal_system.py`:
1. `sort_by_priority_then_time()`, combining my existing separate priority and time sorts into one ordering, since it noticed the next feature would need both dimensions handled together.
2. `find_next_available_slot()`, which converts scheduled tasks' HH:MM times into minute offsets, sorts them into (start, end) intervals, and scans forward from a configurable day-start time looking for the first gap large enough to fit the requested duration.

It also verified the new methods actually ran correctly by writing and executing a small standalone script against real `Owner`/`Pet`/`Task` objects before handing the code back, rather than just generating code and assuming it worked.

**What did you have to verify or fix manually?**

The first version only checked gaps *between* existing tasks, it didn't account for the case where the last task of the day ends early and there's still open time before the day officially ends. I had the agent add a final check against `day_end` after the main loop to cover that case. I confirmed the fix by testing two edge cases myself: an empty task list (should return the day's start time) and a fully booked day (should return `None`), both of which the corrected version handled right.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->
