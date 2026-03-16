import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
pet_age = st.number_input("Pet age", min_value=0, max_value=40, value=3)

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

# Persist domain objects across reruns in a session vault.
if "vault" not in st.session_state:
    st.session_state.vault = {}

vault = st.session_state.vault

if "owner" not in vault:
    vault["owner"] = Owner(name=owner_name)
else:
    vault["owner"].name = owner_name

if "scheduler" not in vault:
    vault["scheduler"] = Scheduler(owner=vault["owner"])
else:
    vault["scheduler"].owner = vault["owner"]

owner: Owner = vault["owner"]
scheduler: Scheduler = vault["scheduler"]

if st.button("Add pet"):
    existing_pet = owner.get_pet(pet_name)
    if existing_pet is None:
        owner.add_pet(Pet(name=pet_name, breed=species, age=int(pet_age)))
        st.success(f"Added pet {pet_name}.")
    else:
        st.info(f"Pet {pet_name} already exists.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], index=1)

if st.button("Add task"):
    if owner.get_pet(pet_name) is None:
        owner.add_pet(Pet(name=pet_name, breed=species, age=int(pet_age)))
    scheduler.add_task(
        pet_name,
        Task(
            action=task_title,
            duration_minutes=int(duration),
            priority=priority,
            frequency=frequency,
        ),
    )
    st.success(f"Added task '{task_title}' for {pet_name}.")

all_tasks = owner.view_tasks()

if all_tasks:
    st.write("Current tasks:")
    task_rows = []
    for pet in owner.pets:
        for task in pet.get_tasks():
            task_rows.append(
                {
                    "pet": pet.name,
                    "title": task.action,
                    "duration_minutes": task.duration_minutes,
                    "priority": task.priority,
                    "frequency": task.frequency,
                    "is_complete": task.is_complete,
                }
            )
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.text("Today's Schedule")
    st.text(scheduler.explain_schedule())

with st.expander("Session vault debug"):
    st.write("Session keys:", list(st.session_state.keys()))
    st.write("Vault keys:", list(vault.keys()))
    st.write("Owner object id:", id(owner))
