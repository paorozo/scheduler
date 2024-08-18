from unittest.mock import MagicMock, patch
from models.task import Task, create_task, get_task
from datetime import datetime, timezone, timedelta


@patch("models.task.SessionLocal")
def test_create_task(mock_session):
    # Mock the database session
    mock_db = MagicMock()
    mock_session.return_value = mock_db

    hours, minutes, seconds = 1, 30, 15
    url = "http://example.com"

    task = create_task(mock_db, hours=hours, minutes=minutes, seconds=seconds, url=url)

    assert task.hours == hours
    assert task.minutes == minutes
    assert task.seconds == seconds
    assert task.url == url
    mock_db.add.assert_called_once_with(task)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(task)


@patch("models.task.SessionLocal")
def test_get_task(mock_session):
    # Mock the database session
    mock_db = MagicMock()
    mock_session.return_value = mock_db

    mock_task = Task(id=1, hours=1, minutes=30, seconds=15, url="http://example.com")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_task

    task = get_task(mock_db, task_id=1)

    assert task.id == 1
    assert task.hours == 1
    assert task.minutes == 30
    assert task.seconds == 15
    assert task.url == "http://example.com"


def test_get_expiration_time():
    task = Task(hours=1, minutes=30, seconds=15, created_at=datetime.now(timezone.utc))
    expiration_time = task.get_expiration_time()

    expected_expiration_time = task.created_at + timedelta(
        hours=1, minutes=30, seconds=15
    )
    assert expiration_time == expected_expiration_time


def test_time_left():
    task = Task(
        hours=0,
        minutes=1,
        seconds=0,
        created_at=datetime.now(timezone.utc) - timedelta(seconds=30),
    )

    time_left = task.time_left()
    assert 29 <= time_left <= 31  # Should be approximately 30 seconds remaining

    # Simulate time expiration
    task.created_at = datetime.now(timezone.utc) - timedelta(minutes=2)

    time_left = task.time_left()
    assert time_left == 0
