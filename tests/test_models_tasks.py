from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, ANY

import pytest

from models.task import Task, create_task, get_task


@pytest.fixture
def mock_db_session():
    # Create a MagicMock object to simulate the database session
    return MagicMock()


def test_create_task(mock_db_session):
    """
    Test the create_task function to ensure that a task is created with the correct values
    """
    hours = 1
    minutes = 30
    seconds = 15
    url = "https://example.com"

    task = create_task(mock_db_session, hours, minutes, seconds, url)

    assert task.url == url
    assert task.created_at <= datetime.now(timezone.utc)
    assert task.expiration_time == task.created_at + timedelta(
        hours=hours, minutes=minutes, seconds=seconds
    )
    assert task.time_left() > 0

    mock_db_session.add.assert_called_once_with(task)
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(task)


def test_get_task(mock_db_session):
    """
    Test the get_task function to ensure that a task is retrieved by ID
    """
    task_id = 1

    expected_task = Task(
        id=task_id,
        url="https://example.com",
        created_at=datetime.now(timezone.utc),
        expiration_time=datetime.now(timezone.utc) + timedelta(hours=1),
        task_triggered=False,
    )

    mock_query = mock_db_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = expected_task

    task = get_task(mock_db_session, task_id)

    assert task == expected_task
    assert task.id == task_id
    assert task.url == "https://example.com"

    mock_db_session.query.assert_called_once_with(Task)
    mock_query.filter.assert_called_once_with(ANY)
    mock_filter.first.assert_called_once()


def test_get_nonexistent_task(mock_db_session):
    """
    Test the get_task function to ensure that None is returned when a task is not found
    """
    task_id = 999
    mock_query = mock_db_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None

    task = get_task(mock_db_session, task_id)

    assert task is None
    mock_db_session.query.assert_called_once_with(Task)
    mock_query.filter.assert_called_once_with(ANY)
    mock_filter.first.assert_called_once()


def test_time_left_after_expiration():
    """
    Test the time_left method of the Task class to ensure that 0 is returned when the task is expired
    """
    expired_task = Task(
        id=1,
        url="https://example.com",
        created_at=datetime.now(timezone.utc) - timedelta(hours=2),
        expiration_time=datetime.now(timezone.utc) - timedelta(hours=1),
        task_triggered=False,
    )

    assert expired_task.time_left() == 0  # Time left should be 0 because it's expired


def test_create_task_failure(mock_db_session):
    """
    Test the create_task function to ensure that an exception is raised when a task cannot be added to the session
    """
    hours = 1
    minutes = 30
    seconds = 15
    url = "https://example.com"

    mock_db_session.add.side_effect = Exception("Failed to add task")

    with pytest.raises(Exception) as excinfo:
        create_task(mock_db_session, hours, minutes, seconds, url)

    assert str(excinfo.value) == "Failed to add task"
    mock_db_session.commit.assert_not_called()
    mock_db_session.refresh.assert_not_called()
