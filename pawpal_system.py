from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    name: str
    category: str
    duration_minutes: int
    priority: str
    recurring: bool = False
    completed: bool = False

    def mark_complete(self):
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def remove_task(self, task_name: str):
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
    def __init__(self, pet: Pet, available_minutes: int):
        self.pet = pet
        self.available_minutes = available_minutes

    def sort_by_priority(self) -> List[Task]:
        pass

    def filter_by_time(self, tasks: List[Task]) -> List[Task]:
        pass

    def generate_plan(self) -> List[Task]:
        pass