from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Pet:
	name: str
	breed: str
	age: int
	tasks: list[Task] = field(default_factory=list)

	def __post_init__(self) -> None:
		if not self.name.strip():
			raise ValueError("Pet name cannot be empty.")
		if not self.breed.strip():
			raise ValueError("Pet breed cannot be empty.")
		if self.age < 0:
			raise ValueError("Pet age cannot be negative.")

	def get_summary(self) -> str:
		year_text = "year" if self.age == 1 else "years"
		return f"{self.name} is a {self.age} {year_text} old {self.breed}."

	def update_age(self, new_age: int) -> None:
		if new_age < 0:
			raise ValueError("Pet age cannot be negative.")
		if new_age < self.age:
			raise ValueError("New age cannot be less than current age.")
		self.age = new_age

	def add_task(self, task: Task) -> None:
		pass

	def remove_task(self, task: Task) -> None:
		pass

	def get_tasks(self) -> list[Task]:
		pass


@dataclass
class Owner:
	name: str
	pets: list[Pet] = field(default_factory=list)

	def add_pet(self, pet: Pet) -> None:
		pass

	def view_tasks(self) -> list[Task]:
		pass


@dataclass
class Task:
	action: str
	duration_minutes: int
	priority: str
	frequency: str
	is_complete: bool = False

	VALID_PRIORITIES = ("low", "medium", "high")
	VALID_FREQUENCIES = ("once", "daily", "weekly")

	def __post_init__(self) -> None:
		if not self.action.strip():
			raise ValueError("Task action cannot be empty.")
		if self.duration_minutes <= 0:
			raise ValueError("Duration must be greater than 0 minutes.")
		if self.priority not in self.VALID_PRIORITIES:
			raise ValueError(f"Priority must be one of: {self.VALID_PRIORITIES}.")
		if self.frequency not in self.VALID_FREQUENCIES:
			raise ValueError(f"Frequency must be one of: {self.VALID_FREQUENCIES}.")

	def set_priority(self, level: str) -> None:
		if level not in self.VALID_PRIORITIES:
			raise ValueError(f"Priority must be one of: {self.VALID_PRIORITIES}.")
		self.priority = level

	def get_duration(self) -> int:
		return self.duration_minutes

	def mark_complete(self) -> None:
		self.is_complete = True


@dataclass
class Scheduler:
	tasks: list[Task] = field(default_factory=list)
	tasks_by_pet: dict[str, list[Task]] = field(default_factory=dict)

	def add_task(self, pet_name: str, task: Task) -> None:
		pass

	def retrieve_tasks(self, pet_name: str | None = None) -> list[Task]:
		pass

	def organize_tasks(self) -> list[Task]:
		pass

	def generate_schedule(self) -> list[Task]:
		pass

	def manage_task_status(self, task: Task, completed: bool) -> None:
		pass

	def explain_schedule(self) -> str:
		pass
