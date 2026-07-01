from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    task = Task(name="Morning walk", category="walk", duration_minutes=30, priority="high")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Biscuit", species="Dog", breed="Golden Retriever")
    assert len(pet.get_tasks()) == 0

    task = Task(name="Feeding", category="feed", duration_minutes=10, priority="high")
    pet.add_task(task)

    assert len(pet.get_tasks()) == 1