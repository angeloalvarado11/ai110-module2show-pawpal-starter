from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Pet:
	name: str
	breed: str
	age: int

	def get_summary(self) -> str:
		pass

	def update_age(self, new_age: int) -> None:
		pass


@dataclass
class Owner:
	name: str
	pet_names: list[str] = field(default_factory=list)
	tasks_to_be_completed: list[Task] = field(default_factory=list)

	def add_pet(self, pet: Pet) -> None:
		pass

	def add_task(self, task: Task) -> None:
		pass

	def view_tasks(self) -> list[Task]:
		pass


@dataclass
class Task:
	action: str
	duration_minutes: int
	priority: str

	def set_priority(self, level: str) -> None:
		pass

	def get_duration(self) -> int:
		pass

	def mark_complete(self) -> None:
		pass


@dataclass
class Plan:
	tasks: list[Task] = field(default_factory=list)
	total_duration: int = 0

	def add_task(self, task: Task) -> None:
		pass

	def calculate_total_duration(self) -> int:
		pass

	def generate_schedule(self) -> list[Task]:
		pass

	def explain_plan(self) -> str:
		pass
