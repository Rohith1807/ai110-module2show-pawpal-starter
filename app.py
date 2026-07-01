import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+, a pet care planning assistant. Add your pets and their
care tasks below, then generate a schedule based on how much time you have today.
"""
)

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

st.divider()

# --- Session state: Owner persists across reruns ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner

st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)
minutes = st.number_input(
    "Available time today (minutes)",
    min_value=0,
    max_value=600,
    value=owner.available_minutes or 60,
    step=5,
)
owner.set_available_minutes(minutes)

st.divider()

# --- Add a pet ---
st.subheader("Add a pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    if pet_name:
        new_pet = Pet(name=pet_name, species=species, breed="")
        owner.add_pet(new_pet)
        st.success(f"Added {pet_name}.")
    else:
        st.warning("Give your pet a name first.")

if not owner.pets:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add tasks to a specific pet ---
if owner.pets:
    st.subheader("Tasks")
    st.caption("Pick a pet, then add a task for them.")

    pet_names = [p.name for p in owner.pets]
    selected_pet_name = st.selectbox("Pet", pet_names)
    selected_pet = next(p for p in owner.pets if p.name == selected_pet_name)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        if task_title:
            new_task = Task(
                name=task_title,
                category="general",
                duration_minutes=int(duration),
                priority=priority,
            )
            selected_pet.add_task(new_task)
            st.success(f"Added '{task_title}' to {selected_pet.name}.")

    # Show tasks per pet
    for pet in owner.pets:
        if pet.get_tasks():
            st.write(f"**{pet.name}'s tasks:**")
            rows = [
                {"title": t.name, "duration_minutes": t.duration_minutes, "priority": t.priority}
                for t in pet.get_tasks()
            ]
            st.table(rows)

st.divider()

# --- Build schedule ---
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    plan, skipped = scheduler.generate_plan()

    if not plan:
        st.warning("No tasks fit in today's schedule. Add some tasks or increase available time.")
    else:
        total_used = 0
        for pet, task in plan:
            total_used += task.duration_minutes
            st.write(f"**[{task.priority.upper()}]** {pet.name}: {task.name} ({task.duration_minutes} min)")
        st.caption(f"Total time used: {total_used}/{owner.available_minutes} minutes")

    if skipped:
        st.markdown("**Skipped (not enough time today):**")
        for pet, task in skipped:
            st.write(f"- {pet.name}: {task.name} ({task.duration_minutes} min)")