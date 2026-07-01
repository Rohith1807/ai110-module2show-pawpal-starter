from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(owner, plan, skipped):
    print("=" * 50)
    print(f"Today's Schedule for {owner.name}")
    print(f"Available time: {owner.available_minutes} minutes")
    print("=" * 50)

    if not plan:
        print("\nNo tasks scheduled today.\n")
    else:
        total_used = 0
        for i, (pet, task) in enumerate(plan, start=1):
            total_used += task.duration_minutes
            print(
                f"{i}. [{task.priority.upper():<6}] {pet.name:<10} "
                f"{task.name:<20} ({task.duration_minutes} min)"
            )
        print(f"\nTotal time used: {total_used}/{owner.available_minutes} minutes")

    if skipped:
        print("\nSkipped (not enough time today):")
        for pet, task in skipped:
            print(f"  - {pet.name}: {task.name} ({task.duration_minutes} min)")

    print("=" * 50)


def print_sorted_by_time(scheduler, tasks):
    print("\n--- Tasks sorted by time ---")
    for pet, task in scheduler.sort_by_time(tasks):
        time_label = task.scheduled_time or "unscheduled"
        print(f"  {time_label} — {pet.name}: {task.name}")


def print_filtered(scheduler, tasks, pet_name):
    print(f"\n--- Tasks for {pet_name} only ---")
    for pet, task in scheduler.filter_tasks(tasks, pet_name=pet_name):
        print(f"  {pet.name}: {task.name} ({task.scheduled_time})")

    print("\n--- Incomplete tasks only ---")
    for pet, task in scheduler.filter_tasks(tasks, completed=False):
        print(f"  {pet.name}: {task.name}")


def print_conflicts(scheduler, tasks):
    print("\n--- Conflict check ---")
    warnings = scheduler.detect_conflicts(tasks)
    if warnings:
        for w in warnings:
            print(f"  WARNING: {w}")
    else:
        print("  No conflicts detected.")


def main():
    owner = Owner(name="Rohith")
    owner.set_available_minutes(60)

    dog = Pet(name="Biscuit", species="Dog", breed="Golden Retriever")
    cat = Pet(name="Whiskers", species="Cat", breed="Tabby")

    owner.add_pet(dog)
    owner.add_pet(cat)

    # Added out of order on purpose to verify sorting works
    dog.add_task(Task(
        name="Feeding", category="feed", duration_minutes=10,
        priority="high", scheduled_time="18:00", frequency="daily",
    ))
    dog.add_task(Task(
        name="Morning walk", category="walk", duration_minutes=30,
        priority="high", scheduled_time="08:00",
    ))
    cat.add_task(Task(
        name="Litter box cleaning", category="grooming", duration_minutes=15,
        priority="medium", scheduled_time="09:00",
    ))
    cat.add_task(Task(
        name="Playtime", category="enrichment", duration_minutes=20,
        priority="low", scheduled_time="08:00",  # same time as the walk, on purpose
    ))

    scheduler = Scheduler(owner)
    all_tasks = owner.get_all_tasks()

    print_sorted_by_time(scheduler, all_tasks)
    print_filtered(scheduler, all_tasks, pet_name="Biscuit")
    print_conflicts(scheduler, all_tasks)

    plan, skipped = scheduler.generate_plan()
    print_schedule(owner, plan, skipped)

    # Demonstrate recurring task automation
    print("\n--- Completing the recurring feeding task ---")
    fed_task = dog.tasks[0]
    new_task = dog.complete_task(fed_task.id)
    if new_task:
        print(f"  Next occurrence created: due {new_task.due_date}, id {new_task.id}")


if __name__ == "__main__":
    main()