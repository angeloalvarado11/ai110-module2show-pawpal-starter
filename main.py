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

scheduler.add_task("Mochi", Task(action="Morning walk",    duration_minutes=30, priority="high",   frequency="daily"))
scheduler.add_task("Mochi", Task(action="Flea medication", duration_minutes=5,  priority="high",   frequency="once"))
scheduler.add_task("Mochi", Task(action="Enrichment play", duration_minutes=20, priority="medium", frequency="daily"))
scheduler.add_task("Luna",  Task(action="Feeding",         duration_minutes=10, priority="high",   frequency="daily"))
scheduler.add_task("Luna",  Task(action="Grooming brush",  duration_minutes=15, priority="low",    frequency="weekly"))

# --- Print today's schedule ---
print()
print("=== Today's Schedule ===")
print(scheduler.explain_schedule())
