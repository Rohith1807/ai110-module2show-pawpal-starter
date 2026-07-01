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


def main():
    owner = Owner(name="Rohith")
    owner.set_available_minutes(60)

    dog = Pet(name="Biscuit", species="Dog", breed="Golden Retriever")
    cat = Pet(name="Whiskers", species="Cat", breed="Tabby")

    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task(name="Morning walk", category="walk", duration_minutes=30, priority="high"))
    dog.add_task(Task(name="Feeding", category="feed", duration_minutes=10, priority="high"))
    cat.add_task(Task(name="Litter box cleaning", category="grooming", duration_minutes=15, priority="medium"))
    cat.add_task(Task(name="Playtime", category="enrichment", duration_minutes=20, priority="low"))

    scheduler = Scheduler(owner)
    plan, skipped = scheduler.generate_plan()

    print_schedule(owner, plan, skipped)


if __name__ == "__main__":
    main()