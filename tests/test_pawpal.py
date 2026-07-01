from datetime import date, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


# --- Fixtures / helpers ---

def make_owner_with_pet(available_minutes=60):
    owner = Owner(name="Rohith")
    owner.set_available_minutes(available_minutes)
    pet = Pet(name="Biscuit", species="Dog", breed="Golden Retriever")
    owner.add_pet(pet)
    return owner, pet


# --- Happy path: sorting ---

def test_sort_by_time_returns_chronological_order():
    owner, pet = make_owner_with_pet()
    pet.add_task(Task(name="Dinner", category="feed", duration_minutes=10,
                       priority="high", scheduled_time="18:00"))
    pet.add_task(Task(name="Walk", category="walk", duration_minutes=20,
                       priority="high", scheduled_time="08:00"))
    pet.add_task(Task(name="Lunch", category="feed", duration_minutes=10,
                       priority="medium", scheduled_time="12:00"))

    scheduler = Scheduler(owner)
    ordered = scheduler.sort_by_time(owner.get_all_tasks())
    times = [task.scheduled_time for _, task in ordered]

    assert times == ["08:00", "12:00", "18:00"]


def test_sort_by_time_places_unscheduled_tasks_last():
    owner, pet = make_owner_with_pet()
    pet.add_task(Task(name="Vet visit", category="meds", duration_minutes=30,
                       priority="high", scheduled_time=None))
    pet.add_task(Task(name="Walk", category="walk", duration_minutes=20,
                       priority="high", scheduled_time="08:00"))

    scheduler = Scheduler(owner)
    ordered = scheduler.sort_by_time(owner.get_all_tasks())

    assert ordered[0][1].name == "Walk"
    assert ordered[-1][1].name == "Vet visit"


# --- Edge case: no tasks ---

def test_sort_by_time_on_pet_with_no_tasks_returns_empty_list():
    owner, pet = make_owner_with_pet()
    scheduler = Scheduler(owner)

    ordered = scheduler.sort_by_time(owner.get_all_tasks())

    assert ordered == []


# --- Filtering ---

def test_filter_tasks_by_pet_name():
    owner = Owner(name="Rohith")
    owner.set_available_minutes(60)
    dog = Pet(name="Biscuit", species="Dog", breed="Golden Retriever")
    cat = Pet(name="Whiskers", species="Cat", breed="Tabby")
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task(name="Walk", category="walk", duration_minutes=20, priority="high"))
    cat.add_task(Task(name="Litter", category="grooming", duration_minutes=10, priority="medium"))

    scheduler = Scheduler(owner)
    dog_only = scheduler.filter_tasks(owner.get_all_tasks(), pet_name="Biscuit")

    assert len(dog_only) == 1
    assert dog_only[0][1].name == "Walk"


def test_filter_tasks_by_completion_status():
    owner, pet = make_owner_with_pet()
    done = Task(name="Feeding", category="feed", duration_minutes=10, priority="high")
    done.mark_complete()
    not_done = Task(name="Walk", category="walk", duration_minutes=20, priority="high")
    pet.add_task(done)
    pet.add_task(not_done)

    scheduler = Scheduler(owner)
    incomplete = scheduler.filter_tasks(owner.get_all_tasks(), completed=False)

    assert len(incomplete) == 1
    assert incomplete[0][1].name == "Walk"


# --- Recurrence logic ---

def test_completing_daily_task_creates_next_occurrence():
    owner, pet = make_owner_with_pet()
    today = date.today()
    task = Task(name="Feeding", category="feed", duration_minutes=10,
                priority="high", frequency="daily", recurring=True, due_date=today)
    pet.add_task(task)

    next_task = pet.complete_task(task.id)

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.completed is False
    assert len(pet.get_tasks()) == 2


def test_completing_one_off_task_creates_no_next_occurrence():
    owner, pet = make_owner_with_pet()
    task = Task(name="Vet visit", category="meds", duration_minutes=30, priority="high")
    pet.add_task(task)

    next_task = pet.complete_task(task.id)

    assert task.completed is True
    assert next_task is None
    assert len(pet.get_tasks()) == 1


# --- Conflict detection ---

def test_detect_conflicts_flags_duplicate_times():
    owner = Owner(name="Rohith")
    owner.set_available_minutes(60)
    dog = Pet(name="Biscuit", species="Dog", breed="Golden Retriever")
    cat = Pet(name="Whiskers", species="Cat", breed="Tabby")
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task(name="Walk", category="walk", duration_minutes=20,
                       priority="high", scheduled_time="08:00"))
    cat.add_task(Task(name="Playtime", category="enrichment", duration_minutes=15,
                       priority="low", scheduled_time="08:00"))

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts(owner.get_all_tasks())

    assert len(warnings) == 1
    assert "08:00" in warnings[0]


def test_detect_conflicts_returns_empty_list_when_no_overlap():
    owner, pet = make_owner_with_pet()
    pet.add_task(Task(name="Walk", category="walk", duration_minutes=20,
                       priority="high", scheduled_time="08:00"))
    pet.add_task(Task(name="Dinner", category="feed", duration_minutes=10,
                       priority="high", scheduled_time="18:00"))

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts(owner.get_all_tasks())

    assert warnings == []


def test_detect_conflicts_does_not_crash_on_unscheduled_tasks():
    owner, pet = make_owner_with_pet()
    pet.add_task(Task(name="Someday task", category="grooming",
                       duration_minutes=15, priority="low", scheduled_time=None))

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts(owner.get_all_tasks())

    assert warnings == []