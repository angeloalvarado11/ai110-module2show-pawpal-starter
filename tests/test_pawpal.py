import pytest
from pawpal_system import Pet, Task


@pytest.fixture
def sample_task() -> Task:
    return Task(action="Morning walk", duration_minutes=30, priority="high", frequency="daily")


@pytest.fixture
def sample_pet() -> Pet:
    return Pet(name="Mochi", breed="Shiba Inu", age=3)


# --- Task Completion ---

def test_task_is_incomplete_by_default(sample_task: Task) -> None:
    assert sample_task.is_complete is False


def test_mark_complete_sets_status_to_true(sample_task: Task) -> None:
    sample_task.mark_complete()
    assert sample_task.is_complete is True


# --- Task Addition ---

def test_new_pet_has_no_tasks(sample_pet: Pet) -> None:
    assert len(sample_pet.get_tasks()) == 0


def test_adding_task_increases_pet_task_count(sample_pet: Pet, sample_task: Task) -> None:
    sample_pet.add_task(sample_task)
    assert len(sample_pet.get_tasks()) == 1


def test_adding_multiple_tasks_increases_count_correctly(sample_pet: Pet) -> None:
    sample_pet.add_task(Task(action="Feed", duration_minutes=10, priority="high", frequency="daily"))
    sample_pet.add_task(Task(action="Grooming", duration_minutes=20, priority="low", frequency="weekly"))
    assert len(sample_pet.get_tasks()) == 2
