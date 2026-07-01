from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import uuid


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
        pass

    def reset(self):
        """Resets a recurring task back to incomplete for the next day."""
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    tasks: List[Task] = field(default_factory=list)
    owner: Optional["Owner"] = None

    def add_task(self, task: Task):
        pass

    def remove_task(self, task_id: str):
        pass

    def get_tasks(self) -> List[Task]:
        pass


@dataclass
class Owner:
    name: str
    available_minutes: int = 0
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        pass

    def set_available_minutes(self, minutes: int):
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def collect_tasks(self) -> List[Task]:
        """Gathers tasks across all of the owner's pets into one list."""
        pass

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        pass

    def filter_by_time(self, tasks: List[Task]) -> Tuple[List[Task], List[Task]]:
        """Returns (scheduled_tasks, skipped_tasks) given owner.available_minutes."""
        pass

    def generate_plan(self) -> Tuple[List[Task], List[Task]]:
        """Runs collect -> sort -> filter in order and returns (plan, skipped)."""
        pass