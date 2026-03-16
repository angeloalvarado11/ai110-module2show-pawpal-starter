from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Pet:
	name: str
	breed: str
	age: int
	tasks: list[Task] = field(default_factory=list)

	def __post_init__(self) -> None:
		"""Validate Pet fields on construction."""
		if not self.name.strip():
			raise ValueError("Pet name cannot be empty.")
		if not self.breed.strip():
			raise ValueError("Pet breed cannot be empty.")
		if self.age < 0:
			raise ValueError("Pet age cannot be negative.")

	def get_summary(self) -> str:
		"""Return a human-readable summary of the pet."""
		year_text = "year" if self.age == 1 else "years"
		return f"{self.name} is a {self.age} {year_text} old {self.breed}."

	def update_age(self, new_age: int) -> None:
		"""Update the pet's age, rejecting negative or decreasing values."""
		if new_age < 0:
			raise ValueError("Pet age cannot be negative.")
		if new_age < self.age:
			raise ValueError("New age cannot be less than current age.")
		self.age = new_age

	def add_task(self, task: Task) -> None:
		"""Append a task to this pet's task list."""
		self.tasks.append(task)

	def remove_task(self, task: Task) -> None:
		"""Remove a specific task from this pet's task list by identity."""
		self.tasks = [t for t in self.tasks if t is not task]

	def get_tasks(self) -> list[Task]:
		"""Return a copy of all tasks assigned to this pet."""
		return list(self.tasks)


@dataclass
class Owner:
	name: str
	pets: list[Pet] = field(default_factory=list)

	def __post_init__(self) -> None:
		"""Validate Owner fields on construction."""
		if not self.name.strip():
			raise ValueError("Owner name cannot be empty.")

	def add_pet(self, pet: Pet) -> None:
		"""Add a Pet to this owner's list of pets."""
		self.pets.append(pet)

	def remove_pet(self, pet_name: str) -> None:
		"""Remove a pet from this owner's list by name."""
		self.pets = [p for p in self.pets if p.name != pet_name]

	def get_pet(self, pet_name: str) -> Pet | None:
		"""Return the Pet with the given name, or None if not found."""
		return next((p for p in self.pets if p.name == pet_name), None)

	def view_tasks(self) -> list[Task]:
		"""Return a flat list of all tasks across every pet this owner manages."""
		return [task for pet in self.pets for task in pet.get_tasks()]


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
		"""Validate Task fields on construction."""
		if not self.action.strip():
			raise ValueError("Task action cannot be empty.")
		if self.duration_minutes <= 0:
			raise ValueError("Duration must be greater than 0 minutes.")
		if self.priority not in self.VALID_PRIORITIES:
			raise ValueError(f"Priority must be one of: {self.VALID_PRIORITIES}.")
		if self.frequency not in self.VALID_FREQUENCIES:
			raise ValueError(f"Frequency must be one of: {self.VALID_FREQUENCIES}.")

	def set_priority(self, level: str) -> None:
		"""Update the task's priority after validating the given level."""
		if level not in self.VALID_PRIORITIES:
			raise ValueError(f"Priority must be one of: {self.VALID_PRIORITIES}.")
		self.priority = level

	def get_duration(self) -> int:
		"""Return the duration of this task in minutes."""
		return self.duration_minutes

	def mark_complete(self) -> None:
		"""Mark this task as completed."""
		self.is_complete = True


@dataclass
class Scheduler:
	owner: Owner

	def add_task(self, pet_name: str, task: Task) -> None:
		"""Add a task to the named pet, raising an error if the pet does not exist."""
		pet = self.owner.get_pet(pet_name)
		if pet is None:
			raise ValueError(f"No pet named '{pet_name}' found for owner '{self.owner.name}'.")
		pet.add_task(task)

	def retrieve_tasks(self, pet_name: str | None = None) -> list[Task]:
		"""Return tasks for a specific pet by name, or all tasks across every pet if no name is given."""
		if pet_name is not None:
			pet = self.owner.get_pet(pet_name)
			if pet is None:
				raise ValueError(f"No pet named '{pet_name}' found for owner '{self.owner.name}'.")
			return pet.get_tasks()
		return self.owner.view_tasks()

	def organize_tasks(self) -> list[Task]:
		"""Return all tasks sorted by priority (high first), then by duration as a tiebreaker."""
		priority_order = {"high": 0, "medium": 1, "low": 2}
		return sorted(
			self.retrieve_tasks(),
			key=lambda t: (priority_order[t.priority], t.duration_minutes),
		)

	def generate_schedule(self) -> list[Task]:
		"""Return the organized list of tasks that have not yet been completed."""
		return [task for task in self.organize_tasks() if not task.is_complete]

	def manage_task_status(self, task: Task, completed: bool) -> None:
		"""Mark a task complete or reset it to incomplete based on the completed flag."""
		if completed:
			task.mark_complete()
		else:
			task.is_complete = False

	def explain_schedule(self) -> str:
		"""Return a human-readable summary of all pending tasks for the owner's pets."""
		scheduled = self.generate_schedule()
		if not scheduled:
			return f"No pending tasks for {self.owner.name}'s pets."
		lines = [f"Schedule for {self.owner.name}:"]
		for task in scheduled:
			lines.append(
				f"  - {task.action} ({task.duration_minutes} min, {task.priority} priority, {task.frequency})"
			)
		return "\n".join(lines)
