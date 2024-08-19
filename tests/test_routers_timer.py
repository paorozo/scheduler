from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@patch("models.task.create_task")
@patch("services.task_service.trigger_webhook")
@patch("datetime.datetime")
def test_set_timer(mock_datetime, mock_trigger_webhook, mock_create_task):
    """
    Test setting a task that will expire in 1 hour
    """
    fixed_now = datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    mock_datetime.now.return_value = fixed_now
    mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.url = "http://example.com"

    mock_create_task.return_value = mock_task

    response = client.post(
        "/timer", params={"hours": 1, "minutes": 0, "seconds": 0, "url": "example.com"}
    )

    assert response.status_code == 200
    assert response.json()["time_left"] == 3599


@patch("models.task.get_task")
def test_get_timer_task_not_found(mock_get_task):
    """
    Test getting a task that does not exist
    """
    mock_get_task.return_value = None

    response = client.get("/timer/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
