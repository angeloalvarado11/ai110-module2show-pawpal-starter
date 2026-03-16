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

### Smarter Scheduling

The following features were added to `pawpal_system.py` to make the scheduler more useful for real pet care routines:

**Priority + duration sorting (`Scheduler.organize_tasks`)**
Tasks are sorted using a two-key lambda: priority tier first (`high → medium → low`), then `duration_minutes` as a tiebreaker. This ensures the most important tasks always appear at the top of the schedule, with shorter tasks surfacing before longer ones when priority is equal.

**Task filtering (`Scheduler.filter_tasks`)**
Tasks can be filtered by completion status, pet name, or both. Pass `completed=True` to see what's done, `completed=False` for what's still pending, and `pet_name="Mochi"` to scope results to a specific pet. Filters can be combined freely.

**Automatic next occurrence (`Task.next_occurrence`)**
When a recurring task is marked complete, a new instance is automatically created for the next occurrence using Python's `timedelta`:
- `"daily"` tasks get a new due date of today + 1 day
- `"weekly"` tasks get today + 7 days
- `"once"` tasks return `None` — no follow-up is created

**Auto-spawn on completion (`Scheduler.manage_task_status`)**
Calling `manage_task_status(task, completed=True, pet_name="Mochi")` marks the task done and automatically adds the next occurrence to that pet's task list if the task is recurring. Passing `pet_name` is optional — omitting it marks complete without spawning.
