import pytest
from datetime import date, timedelta
from pawpal_system import Owner, Pet, Scheduler, Task


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


# --- Task Filtering ---

def test_filter_tasks_by_completion_status() -> None:
    owner = Owner(name="Jordan")
    mochi = Pet(name="Mochi", breed="Shiba Inu", age=3)
    owner.add_pet(mochi)
    scheduler = Scheduler(owner=owner)

    done_task = Task(action="Feed", duration_minutes=10, priority="high", frequency="daily")
    done_task.mark_complete()
    todo_task = Task(action="Walk", duration_minutes=20, priority="medium", frequency="daily")

    scheduler.add_task("Mochi", done_task)
    scheduler.add_task("Mochi", todo_task)

    completed = scheduler.filter_tasks(completed=True)
    pending = scheduler.filter_tasks(completed=False)

    assert completed == [done_task]
    assert pending == [todo_task]


def test_filter_tasks_by_pet_name() -> None:
    owner = Owner(name="Jordan")
    mochi = Pet(name="Mochi", breed="Shiba Inu", age=3)
    luna = Pet(name="Luna", breed="Tabby Cat", age=5)
    owner.add_pet(mochi)
    owner.add_pet(luna)
    scheduler = Scheduler(owner=owner)

    mochi_task = Task(action="Walk", duration_minutes=20, priority="high", frequency="daily")
    luna_task = Task(action="Brush", duration_minutes=15, priority="low", frequency="weekly")

    scheduler.add_task("Mochi", mochi_task)
    scheduler.add_task("Luna", luna_task)

    assert scheduler.filter_tasks(pet_name="Mochi") == [mochi_task]


# --- Next Occurrence ---

def test_once_task_next_occurrence_returns_none() -> None:
    task = Task(action="Flea medication", duration_minutes=5, priority="high", frequency="once")
    assert task.next_occurrence() is None


def test_daily_task_next_occurrence_is_one_day_later() -> None:
    today = date.today()
    task = Task(action="Morning walk", duration_minutes=30, priority="high", frequency="daily", due_date=today)
    next_task = task.next_occurrence()
    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.is_complete is False


def test_weekly_task_next_occurrence_is_seven_days_later() -> None:
    today = date.today()
    task = Task(action="Grooming", duration_minutes=15, priority="low", frequency="weekly", due_date=today)
    next_task = task.next_occurrence()
    assert next_task is not None
    assert next_task.due_date == today + timedelta(weeks=1)


def test_completing_daily_task_spawns_next_occurrence_in_scheduler() -> None:
    owner = Owner(name="Jordan")
    owner.add_pet(Pet(name="Mochi", breed="Shiba Inu", age=3))
    scheduler = Scheduler(owner=owner)
    task = Task(action="Morning walk", duration_minutes=30, priority="high", frequency="daily")
    scheduler.add_task("Mochi", task)

    scheduler.manage_task_status(task, completed=True, pet_name="Mochi")

    all_tasks = scheduler.retrieve_tasks("Mochi")
    assert len(all_tasks) == 2
    new_task = next(t for t in all_tasks if not t.is_complete)
    assert new_task.due_date == date.today() + timedelta(days=1)


# --- Failing Scenarios (invalid input should raise ValueError) ---

def test_task_with_empty_action_raises() -> None:
    with pytest.raises(ValueError):
        Task(action="", duration_minutes=10, priority="high", frequency="daily")


def test_task_with_zero_duration_raises() -> None:
    with pytest.raises(ValueError):
        Task(action="Walk", duration_minutes=0, priority="high", frequency="daily")


def test_task_with_negative_duration_raises() -> None:
    with pytest.raises(ValueError):
        Task(action="Walk", duration_minutes=-5, priority="high", frequency="daily")


def test_task_with_invalid_priority_raises() -> None:
    with pytest.raises(ValueError):
        Task(action="Walk", duration_minutes=10, priority="urgent", frequency="daily")


def test_task_with_invalid_frequency_raises() -> None:
    with pytest.raises(ValueError):
        Task(action="Walk", duration_minutes=10, priority="high", frequency="monthly")


def test_filter_tasks_with_nonexistent_pet_raises() -> None:
    owner = Owner(name="Jordan")
    scheduler = Scheduler(owner=owner)
    with pytest.raises(ValueError):
        scheduler.filter_tasks(pet_name="Ghost")


def test_add_task_to_nonexistent_pet_raises() -> None:
    owner = Owner(name="Jordan")
    scheduler = Scheduler(owner=owner)
    with pytest.raises(ValueError):
        scheduler.add_task("Ghost", Task(action="Walk", duration_minutes=20, priority="high", frequency="daily"))


def test_pet_with_negative_age_raises() -> None:
    with pytest.raises(ValueError):
        Pet(name="Mochi", breed="Shiba Inu", age=-1)


def test_owner_with_empty_name_raises() -> None:
    with pytest.raises(ValueError):
        Owner(name="")
