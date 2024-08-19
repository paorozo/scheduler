import pytest
from unittest.mock import MagicMock, ANY
from datetime import datetime, timedelta, timezone

from models.task import Task, create_task, get_task


@pytest.fixture
def mock_db_session():
    # Create a MagicMock object to simulate the database session
    return MagicMock()


def test_create_task(mock_db_session):
    # Setup input data
    hours = 1
    minutes = 30
    seconds = 15
    url = "https://example.com"

    # Call the create_task function with the mock
    task = create_task(mock_db_session, hours, minutes, seconds, url)

    # Assertions
    assert task.url == url
    assert task.created_at <= datetime.now(timezone.utc)
    assert task.expiration_time == task.created_at + timedelta(
        hours=hours, minutes=minutes, seconds=seconds
    )
    assert task.time_left() > 0

    # Ensure that the database session methods were called
    mock_db_session.add.assert_called_once_with(task)
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(task)


def test_get_task(mock_db_session):
    # Setup input data
    task_id = 1

    # Configure the expected return when querying by ID
    expected_task = Task(
        id=task_id,
        url="https://example.com",
        created_at=datetime.now(timezone.utc),
        expiration_time=datetime.now(timezone.utc) + timedelta(hours=1),
        task_triggered=False,
    )
    # Mock the query method chain
    mock_query = mock_db_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = expected_task

    # Call the get_task function with the mock
    task = get_task(mock_db_session, task_id)

    # Assertions
    assert task == expected_task
    assert task.id == task_id
    assert task.url == "https://example.com"

    # Ensure that the correct query was made
    mock_db_session.query.assert_called_once_with(Task)
    mock_query.filter.assert_called_once_with(ANY)
    mock_filter.first.assert_called_once()


def test_get_nonexistent_task(mock_db_session):
    # Setup input data
    task_id = 999  # Assuming this task ID does not exist

    # Mock the query method chain to return None
    mock_query = mock_db_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None

    # Call the get_task function with the mock
    task = get_task(mock_db_session, task_id)

    # Assertions
    assert task is None  # The task should not be found

    # Ensure that the correct query was made
    mock_db_session.query.assert_called_once_with(Task)
    mock_query.filter.assert_called_once_with(ANY)
    mock_filter.first.assert_called_once()


def test_time_left_after_expiration():
    # Setup a task that has already expired
    expired_task = Task(
        id=1,
        url="https://example.com",
        created_at=datetime.now(timezone.utc) - timedelta(hours=2),
        expiration_time=datetime.now(timezone.utc) - timedelta(hours=1),
        task_triggered=False,
    )

    # Assertions
    assert expired_task.time_left() == 0  # Time left should be 0 because it's expired


def test_create_task_failure(mock_db_session):
    # Setup input data
    hours = 1
    minutes = 30
    seconds = 15
    url = "https://example.com"

    # Simulate a failure when adding a task to the session
    mock_db_session.add.side_effect = Exception("Failed to add task")

    # Call the create_task function with the mock and catch the exception
    with pytest.raises(Exception) as excinfo:
        create_task(mock_db_session, hours, minutes, seconds, url)

    # Assertions
    assert str(excinfo.value) == "Failed to add task"

    # Ensure that commit and refresh were not called due to the failure
    mock_db_session.commit.assert_not_called()
    mock_db_session.refresh.assert_not_called()
