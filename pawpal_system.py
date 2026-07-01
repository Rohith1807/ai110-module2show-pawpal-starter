from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import uuid


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    name: str
    category: str
    duration_minutes: int
    priority: str
    recurring: bool = False
    completed: bool = False
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])

    def mark_complete(self):
        """Marks this task as completed."""
        self.completed = True

    def reset(self):
        """Resets a recurring task back to incomplete for the next day."""
        if self.recurring:
            self.completed = False


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    tasks: List[Task] = field(default_factory=list)
    owner: Optional["Owner"] = None

    def add_task(self, task: Task):
        """Adds a new task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task_id: str):
        """Removes a task from this pet's task list by its unique id."""
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def get_tasks(self) -> List[Task]:
        """Returns this pet's current list of tasks."""
        return self.tasks


@dataclass
class Owner:
    name: str
    available_minutes: int = 0
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Adds a pet to this owner and links the pet back to the owner."""
        pet.owner = self
        self.pets.append(pet)

    def set_available_minutes(self, minutes: int):
        """Sets how many minutes the owner has available for tasks today."""
        self.available_minutes = minutes

    def get_all_tasks(self) -> List[Tuple[Pet, Task]]:
        """Flattens tasks across all pets, paired with their owning pet."""
        all_tasks = []
        for pet in self.pets:
            for task in pet.get_tasks():
                all_tasks.append((pet, task))
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner):
        """Builds a scheduler for a given owner and their pets."""
        self.owner = owner

    def collect_tasks(self) -> List[Tuple[Pet, Task]]:
        """Pulls all incomplete tasks across the owner's pets."""
        return [
            (pet, task)
            for pet, task in self.owner.get_all_tasks()
            if not task.completed
        ]

    def sort_by_priority(
        self, tasks: List[Tuple[Pet, Task]]
    ) -> List[Tuple[Pet, Task]]:
        """Sorts tasks by priority first, then by duration as a tiebreaker."""
        return sorted(
            tasks,
            key=lambda pt: (PRIORITY_ORDER.get(pt[1].priority, 99), -pt[1].duration_minutes),
        )

    def filter_by_time(
        self, tasks: List[Tuple[Pet, Task]]
    ) -> Tuple[List[Tuple[Pet, Task]], List[Tuple[Pet, Task]]]:
        """Greedily fits tasks into the owner's time budget, returning (scheduled, skipped)."""
        scheduled = []
        skipped = []
        remaining = self.owner.available_minutes

        for pet, task in tasks:
            if task.duration_minutes <= remaining:
                scheduled.append((pet, task))
                remaining -= task.duration_minutes
            else:
                skipped.append((pet, task))

        return scheduled, skipped

    def generate_plan(self) -> Tuple[List[Tuple[Pet, Task]], List[Tuple[Pet, Task]]]:
        """Runs collect, sort, then filter in that fixed order to build today's plan."""
        tasks = self.collect_tasks()
        sorted_tasks = self.sort_by_priority(tasks)
        return self.filter_by_time(sorted_tasks)