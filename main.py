from pawpal_system import Owner, Pet, Scheduler, Task

# --- Setup owner and pets ---
owner = Owner(name="Jordan")

mochi = Pet(name="Mochi", breed="Shiba Inu", age=3)
luna = Pet(name="Luna", breed="Tabby Cat", age=5)

owner.add_pet(mochi)
owner.add_pet(luna)

# --- Print pet summaries ---
print("=== Pets ===")
for pet in owner.pets:
    print(pet.get_summary())

# --- Add tasks to pets ---
scheduler = Scheduler(owner=owner)


# Add tasks intentionally out of order to verify sorting.
mochi_tasks = [
    Task(action="Enrichment play", duration_minutes=20, priority="medium", frequency="daily"),
    Task(action="Flea medication", duration_minutes=5, priority="high", frequency="once"),
    Task(action="Morning walk", duration_minutes=30, priority="high", frequency="daily"),
]

luna_tasks = [
    Task(action="Grooming brush", duration_minutes=15, priority="low", frequency="weekly"),
    Task(action="Feeding", duration_minutes=10, priority="high", frequency="daily"),
]

for task in mochi_tasks:
    scheduler.add_task("Mochi", task)

for task in luna_tasks:
    scheduler.add_task("Luna", task)

# Mark one task complete so completion filtering can be demonstrated.
scheduler.manage_task_status(mochi_tasks[1], completed=True)

print()
print("=== Organize Tasks (priority, then duration) ===")
for task in scheduler.organize_tasks():
    print(f"- {task.action} ({task.priority}, {task.duration_minutes} min, complete={task.is_complete})")

print()
print("=== Filter Tasks: Pending Only ===")
for task in scheduler.filter_tasks(completed=False):
    print(f"- {task.action} ({task.priority}, {task.duration_minutes} min)")

print()
print("=== Filter Tasks: Completed Only ===")
for task in scheduler.filter_tasks(completed=True):
    print(f"- {task.action} ({task.priority}, {task.duration_minutes} min)")

print()
print("=== Filter Tasks: Mochi Only ===")
for task in scheduler.filter_tasks(pet_name="Mochi"):
    print(f"- {task.action} ({task.priority}, {task.duration_minutes} min, complete={task.is_complete})")

# --- Print today's schedule ---
print()
print("=== Today's Schedule ===")
print(scheduler.explain_schedule())
